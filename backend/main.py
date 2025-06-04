from __future__ import annotations

import os
import sqlite3
from datetime import time
from fastapi import FastAPI, HTTPException, Request
import logging
from pydantic import BaseModel

from src import auth, mindful, dashboard, relationships, activity, notifications, subscriptions, sessions as session_models
from src import monitoring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mindful")

app = FastAPI()

db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgresql"):
    import psycopg2
    conn = psycopg2.connect(db_url)
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
notify_manager = notifications.NotificationManager()

class SignUp(BaseModel):
    email: str
    password: str
    display_name: str | None = None

class Login(BaseModel):
    email: str
    password: str

class SessionInput(BaseModel):
    user_id: int
    date: str
    time: str | None = None
    duration: int
    type: str
    location: str | None = None
    notes: str | None = None
    moodBefore: int | None = None
    moodAfter: int | None = None

class FollowInput(BaseModel):
    follower_id: int
    followed_id: int

class NotificationInput(BaseModel):
    user_id: int
    reminder_time: str
    message: str

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
    return {"user_id": row[0]}

@app.post('/sessions')
def create_session(info: SessionInput):
    session_id = mindful.log_session(
        conn,
        info.user_id,
        info.duration,
        info.type,
        info.date,
        session_time=info.time,
        location=info.location,
        notes=info.notes,
        mood_before=info.moodBefore,
        mood_after=info.moodAfter,
    )
    feed.log_session(info.user_id, f"{info.type} {info.duration}m")
    return {"session_id": session_id}

@app.get('/dashboard/{user_id}')
def get_dashboard(user_id: int):
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
            session_date=r[2],
            location=r[4] or ''
        )
        for r in records
    ]
    total = dashboard.calculate_total_time(sess)
    count = dashboard.calculate_session_count(sess)
    streak = dashboard.calculate_current_streak(sess)
    return {"total": total, "sessions": count, "streak": streak}

@app.get('/feed/{user_id}')
def get_feed(user_id: int):
    items = feed.get_feed(user_id)
    return [item.__dict__ for item in items]

@app.post('/follow')
def follow(data: FollowInput):
    relationships.follow_user(conn, data.follower_id, data.followed_id)
    return {"status": "ok"}

@app.post('/unfollow')
def unfollow(data: FollowInput):
    relationships.unfollow_user(conn, data.follower_id, data.followed_id)
    return {"status": "ok"}

@app.post('/notifications')
def add_notification(data: NotificationInput):
    t = time.fromisoformat(data.reminder_time)
    note_id = notify_manager.add_notification(data.user_id, t, data.message)
    return {"notification_id": note_id}

@app.get('/notifications/{user_id}')
def list_notifications(user_id: int):
    notes = notify_manager.get_notifications(user_id)
    return [n.__dict__ for n in notes]


class JoinChallengeInput(BaseModel):
    user_id: int
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
def join_challenge(data: JoinChallengeInput):
    mindful.join_challenge(conn, data.user_id, data.challenge_id)
    return {"status": "ok"}


@app.get('/moods/{user_id}')
def get_moods(user_id: int):
    moods = mindful.get_user_moods(conn, user_id)
    return [
        {"before": m[0], "after": m[1]} for m in moods
    ]


class SubscriptionUpdate(BaseModel):
    tier: str


@app.get('/subscriptions/{user_id}')
def get_subscription(user_id: int):
    tier = subscriptions.get_user_tier(conn, user_id)
    return {"tier": tier}


@app.post('/subscriptions/{user_id}')
def update_subscription(user_id: int, data: SubscriptionUpdate):
    subscriptions.subscribe_user(conn, user_id, data.tier, '2023-01-01')
    return {"status": "ok"}
