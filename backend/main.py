from __future__ import annotations

import os
import sqlite3
  
from datetime import time
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from jose import JWTError, jwt
import logging
from pydantic import BaseModel

from src import auth, mindful, dashboard, relationships, activity, notifications, subscriptions, sessions as session_models
from src import monitoring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mindful")

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"

app = FastAPI()

db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgresql"):
    import psycopg2
    from src.pgutil import PGConnectionWrapper

    raw_conn = psycopg2.connect(db_url)
    conn = PGConnectionWrapper(raw_conn)
    mindful.init_postgres_db(conn)
else:
    db_file = os.getenv("DB_FILE", "mindful.db")
    conn = sqlite3.connect(db_file, check_same_thread=False)
    mindful.init_db(conn)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Completed %s", response.status_code)
    return response

feed = activity.ActivityFeed()
notify_manager = notifications.NotificationManager(conn)


def get_current_user(authorization: str = Header(None)) -> int:
    """Return the authenticated user's ID from a Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id)

class SignUp(BaseModel):
    email: str
    password: str
    display_name: str | None = None

class Login(BaseModel):
    email: str
    password: str

class SessionInput(BaseModel):
    date: str
    time: str | None = None
    duration: int
    type: str
    location: str | None = None
    notes: str | None = None
    moodBefore: int | None = None
    moodAfter: int | None = None

class FollowInput(BaseModel):
    followed_id: int

class NotificationInput(BaseModel):
    reminder_time: str
    message: str
    enabled: bool = True

@app.post('/auth/signup')
def signup(data: SignUp):
    user_id = auth.register_user(conn, data.email, data.password, display_name=data.display_name)
    monitoring.log_event("signup", {"user": user_id})
    return {"user_id": user_id}

@app.post('/auth/login')
def login(data: Login):
    cur = conn.execute('SELECT id, password_hash FROM users WHERE email = ?', (data.email,))
    row = cur.fetchone()
    if not row or auth.hash_password(data.password) != row[1]:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    monitoring.log_event("login", {"user": row[0]})
    token = jwt.encode({"user_id": row[0]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

@app.post('/sessions')
def create_session(info: SessionInput, user_id: int = Depends(get_current_user)):
    session_id = mindful.log_session(
        conn,
        user_id,
        info.duration,
        info.type,
        info.date,
        session_time=info.time,
        location=info.location,
        notes=info.notes,
        mood_before=info.moodBefore,
        mood_after=info.moodAfter,
    )
    feed.log_session(user_id, f"{info.type} {info.duration}m")
    return {"session_id": session_id}

@app.get('/dashboard/{user_id}')
def get_dashboard(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    cur = conn.execute(
        'SELECT duration, session_type, session_date, session_time, location FROM sessions WHERE user_id = ?',
        (user_id,)
    )
    records = cur.fetchall()
    sess = [
        session_models.MeditationSession(
            r[0],
            r[1],
            time.fromisoformat(r[3]) if r[3] else time(0, 0),
            session_date=date.fromisoformat(r[2]) if isinstance(r[2], str) else r[2],
            location=r[4] or ''
        )
        for r in records
    ]
    total = dashboard.calculate_total_time(sess)
    count = dashboard.calculate_session_count(sess)
    streak = dashboard.calculate_current_streak(sess)
    return {"total": total, "sessions": count, "streak": streak}

@app.get('/feed/{user_id}')
def get_feed(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    items = feed.get_feed(user_id)
    return [item.__dict__ for item in items]

@app.post('/follow')
def follow(data: FollowInput, user_id: int = Depends(get_current_user)):
    relationships.follow_user(conn, user_id, data.followed_id)
    return {"status": "ok"}

@app.post('/unfollow')
def unfollow(data: FollowInput, user_id: int = Depends(get_current_user)):
    relationships.unfollow_user(conn, user_id, data.followed_id)
    return {"status": "ok"}

@app.post('/notifications')
def add_notification(data: NotificationInput, user_id: int = Depends(get_current_user)):
    t = time.fromisoformat(data.reminder_time)
    note_id = notify_manager.add_notification(user_id, t, data.message)
    return {"notification_id": note_id}

@app.get('/notifications/{user_id}')
def list_notifications(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    notes = notify_manager.get_notifications(user_id)
    return [n.__dict__ for n in notes]


class JoinChallengeInput(BaseModel):
    challenge_id: int


@app.get('/challenges')
def list_challenges():
    cur = conn.execute(
        'SELECT id, name, target_minutes, start_date, end_date FROM community_challenges'
    )
    rows = cur.fetchall()
    return [
        {
            'id': r[0],
            'name': r[1],
            'target_minutes': r[2],
            'start_date': r[3],
            'end_date': r[4],
        }
        for r in rows
    ]


@app.post('/challenges/join')
def join_challenge(data: JoinChallengeInput, user_id: int = Depends(get_current_user)):
    mindful.join_challenge(conn, user_id, data.challenge_id)
    return {"status": "ok"}


@app.get('/moods/{user_id}')
def get_moods(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    moods = mindful.get_user_moods(conn, user_id)
    return [
        {"before": m[0], "after": m[1]} for m in moods
    ]


class SubscriptionUpdate(BaseModel):
    tier: str


@app.get('/subscriptions/{user_id}')
def get_subscription(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    tier = subscriptions.get_user_tier(conn, user_id)
    return {"tier": tier}


@app.post('/subscriptions/{user_id}')
def update_subscription(user_id: int, data: SubscriptionUpdate, current_user: int = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail='Forbidden')
    subscriptions.subscribe_user(conn, user_id, data.tier, '2023-01-01')
    return {"status": "ok"}
