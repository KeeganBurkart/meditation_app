from __future__ import annotations

import os
import sqlite3
from datetime import time, date
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt as jose_jwt
from pathlib import Path
from uuid import uuid4

import logging
from pydantic import BaseModel

from src import auth, mindful, dashboard, relationships, activity, notifications, subscriptions, sessions as session_models, profiles
from src import monitoring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mindful")

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret") # Changed default for clarity
ALGORITHM = "HS256"

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

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
    logger.info("%s %s %s", request.method, request.url.path, request.query_params)
    response = await call_next(request)
    logger.info("Completed %s %s", request.method, request.url.path) # Removed status code as it's in response
    return response

# Assuming ActivityFeed and NotificationManager classes were updated to accept 'conn'
feed = activity.ActivityFeed(conn)
notify_manager = notifications.NotificationManager(conn)


def get_current_user(authorization: str = Header(None)) -> int:
    """Return the authenticated user's ID from a Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated: Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")
        if user_id_from_token is None: # Check if user_id key exists and is not None
            raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id_from_token)

class SignUp(BaseModel):
    email: str
    password: str
    display_name: str | None = None

class Login(BaseModel):
    email: str
    password: str

class SessionInput(BaseModel):
    date: str # Expect ISO format string e.g. "YYYY-MM-DD"
    time: str | None = None # Expect ISO format string e.g. "HH:MM" or "HH:MM:SS"
    duration: int
    type: str
    location: str | None = None
    notes: str | None = None
    moodBefore: int | None = None
    moodAfter: int | None = None

class FollowInput(BaseModel):
    followed_id: int

class NotificationInput(BaseModel):
    reminder_time: str # Expect ISO format string e.g. "HH:MM" or "HH:MM:SS"
    message: str
    enabled: bool = True # Added from one of the versions

class BioUpdate(BaseModel):
    bio: str

# Removed redundant BioUpdate class definition that was present in the conflict

@app.post('/auth/signup')
def signup_user(data: SignUp): # Renamed for clarity from just 'signup'
    user_id = auth.register_user(conn, data.email, data.password, display_name=data.display_name)
    monitoring.log_event("signup", {"user": user_id})
    return {"user_id": user_id}

@app.post('/auth/login')
def login_user(data: Login): # Renamed for clarity
    cur = conn.execute('SELECT id, password_hash FROM users WHERE email = ?', (data.email,))
    row = cur.fetchone()
    if not row or row[1] is None or not auth.verify_password(data.password, row[1]):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    user_id = row[0]
    monitoring.log_event("login", {"user": user_id})
    token_payload = {"user_id": user_id}
    token = jose_jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"} # Added token_type

@app.post('/sessions', response_model=dict) # Added response_model
def create_session(info: SessionInput, current_user_id: int = Depends(get_current_user)):
    session_id = mindful.log_session(
        conn,
        current_user_id, # Use current_user_id from token
        info.duration,
        info.type,
        info.date,
        session_time=info.time,
        location=info.location,
        notes=info.notes,
        mood_before=info.moodBefore,
        mood_after=info.moodAfter,
    )
    # Assuming feed.log_session was updated to work with DB
    # and potentially accepts session_id
    feed.log_session(current_user_id, f"{info.type} {info.duration}m", session_id)
    return {"session_id": session_id}

@app.get('/dashboard/{user_id_param}', response_model=dict) # Added response_model, renamed path param
def get_dashboard_data(user_id_param: int, current_user_id: int = Depends(get_current_user)): # Renamed
    if user_id_param != current_user_id:
        raise HTTPException(status_code=403, detail='Forbidden: Cannot access another user\'s dashboard')
    cur = conn.execute(
        'SELECT duration, session_type, session_date, session_time, location FROM sessions WHERE user_id = ?',
        (user_id_param,) # Use user_id_param from path
    )
    records = cur.fetchall()
    sess = [
        session_models.MeditationSession(
            duration_minutes=r[0],
            meditation_type=r[1],
            time_of_day=time.fromisoformat(r[3]) if r[3] else time(0, 0),
            # Ensure r[2] (session_date) is a date object or string that can be parsed
            session_date=date.fromisoformat(r[2]) if isinstance(r[2], str) else r[2],
            location=r[4] or ''
        )
        for r in records
    ]
    total = dashboard.calculate_total_time(sess)
    count = dashboard.calculate_session_count(sess)
    streak = dashboard.calculate_current_streak(sess)
    return {"total_time": total, "session_count": count, "current_streak": streak} # More descriptive keys

@app.get('/feed', response_model=list) # Changed path to /feed, user_id from token
def get_user_feed(current_user_id: int = Depends(get_current_user)):
    # This is the implementation from the third provided diff for /feed
    followed_ids = relationships.get_following(conn, current_user_id)
    # User should also see their own items in their feed
    user_ids_for_feed = set(followed_ids)
    user_ids_for_feed.add(current_user_id)

    if not user_ids_for_feed:
        return []

    placeholders = ",".join("?" for _ in user_ids_for_feed)
    # Assumes 'feed_items' table and 'users.is_public' column exist
    # This query needs to be adapted if ActivityFeed class handles DB querying directly
    query = (
        "SELECT f.id, f.user_id, u.display_name, f.item_type, f.message, f.timestamp, f.target_user_id "
        "FROM feed_items f JOIN users u ON f.user_id = u.id "
        f"WHERE f.user_id IN ({placeholders}) AND (u.is_public = 1 OR f.user_id = ?) " # Check privacy or own item
        "ORDER BY f.timestamp DESC, f.id DESC LIMIT 20" # Increased limit
    )
    params = (*list(user_ids_for_feed), current_user_id)
    cur = conn.execute(query, params)
    rows = cur.fetchall()
    return [
        {
            "item_id": r[0],
            "user_id": r[1],
            "user_display_name": r[2],
            "item_type": r[3],
            "message": r[4],
            "timestamp": r[5].isoformat() if isinstance(r[5], (date, time)) else r[5], # Ensure ISO format
            "target_user_id": r[6],
        }
        for r in rows
    ]


@app.post('/follow', response_model=dict)
def follow_user_action(data: FollowInput, current_user_id: int = Depends(get_current_user)): # Renamed
    if current_user_id == data.followed_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    relationships.follow_user(conn, current_user_id, data.followed_id)
    return {"status": "ok", "message": f"User {current_user_id} now follows {data.followed_id}"}

@app.post('/unfollow', response_model=dict)
def unfollow_user_action(data: FollowInput, current_user_id: int = Depends(get_current_user)): # Renamed
    relationships.unfollow_user(conn, current_user_id, data.followed_id)
    return {"status": "ok", "message": f"User {current_user_id} unfollowed {data.followed_id}"}

@app.post('/notifications', response_model=dict)
def add_user_notification(data: NotificationInput, current_user_id: int = Depends(get_current_user)): # Renamed
    try:
        reminder_time_obj = time.fromisoformat(data.reminder_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid reminder_time format. Use HH:MM or HH:MM:SS.")
    note_id = notify_manager.add_notification(current_user_id, reminder_time_obj, data.message, data.enabled)
    return {"notification_id": note_id}

@app.get('/notifications', response_model=list) # Changed path, user_id from token
def list_user_notifications(current_user_id: int = Depends(get_current_user)): # Renamed
    notes = notify_manager.get_notifications(current_user_id)
    return [n.dict() if hasattr(n, 'dict') else n.__dict__ for n in notes] # Use .dict() if Pydantic model


class JoinChallengeInput(BaseModel):
    challenge_id: int

@app.get('/challenges', response_model=list) # Added response_model
def list_community_challenges(): # Renamed
    cur = conn.execute(
        'SELECT id, name, target_minutes, start_date, end_date FROM community_challenges'
    )
    rows = cur.fetchall()
    return [
        {
            'id': r[0],
            'name': r[1],
            'target_minutes': r[2],
            'start_date': r[3].isoformat() if isinstance(r[3], date) else r[3], # Ensure ISO format
            'end_date': r[4].isoformat() if isinstance(r[4], date) else r[4], # Ensure ISO format
        }
        for r in rows
    ]

@app.post('/challenges/join', response_model=dict) # Added response_model
def join_community_challenge(data: JoinChallengeInput, current_user_id: int = Depends(get_current_user)): # Renamed
    mindful.join_challenge(conn, current_user_id, data.challenge_id)
    return {"status": "ok", "message": f"User {current_user_id} joined challenge {data.challenge_id}"}

@app.get('/moods', response_model=list) # Changed path, user_id from token
def get_user_moods(current_user_id: int = Depends(get_current_user)): # Renamed
    moods = mindful.get_user_moods(conn, current_user_id)
    return [
        {"before": m[0], "after": m[1]} for m in moods
    ]

class SubscriptionUpdate(BaseModel):
    tier: str

@app.get('/subscriptions/me', response_model=dict) # Changed path for current user
def get_my_subscription(current_user_id: int = Depends(get_current_user)): # Renamed
    tier = subscriptions.get_user_tier(conn, current_user_id)
    return {"tier": tier}

@app.put('/subscriptions/me', response_model=dict) # Changed to PUT, path for current user
def update_my_subscription(data: SubscriptionUpdate, current_user_id: int = Depends(get_current_user)): # Renamed
    # Assuming start_date is current date or handled by subscribe_user
    subscriptions.subscribe_user(conn, current_user_id, data.tier, date.today().isoformat())
    return {"status": "ok", "tier": data.tier}

@app.put('/users/me/bio', response_model=dict) # Path for current user
def update_my_bio(data: BioUpdate, current_user_id: int = Depends(get_current_user)): # Renamed
    profiles.update_bio(conn, current_user_id, data.bio) # Assuming profiles.update_bio exists
    return {"status": "ok", "message": "Bio updated successfully."}

@app.post('/users/me/photo', response_model=dict) # Path for current user
async def upload_my_photo(request: Request, current_user_id: int = Depends(get_current_user)): # Renamed
    content_type = request.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
         raise HTTPException(status_code=400, detail="Invalid content type, please upload an image.")

    file_data = await request.body()
    if not file_data:
        raise HTTPException(status_code=400, detail="No image data received.")

    # Basic filename generation, consider more robust naming/extension handling
    original_filename = request.headers.get("X-Filename", f"photo_{current_user_id}")
    ext = Path(original_filename).suffix or ".jpg" # Default to .jpg if no extension
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif"]: # Basic extension validation
        raise HTTPException(status_code=400, detail="Unsupported image format. Please use JPG, PNG, or GIF.")

    filename = f"{uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    try:
        with open(dest, 'wb') as out_file:
            out_file.write(file_data)
    except IOError:
        logger.error(f"IOError saving uploaded photo to {dest}")
        raise HTTPException(status_code=500, detail="Could not save uploaded photo.")

    photo_url = f"/uploads/{filename}"
    profiles.update_photo(conn, current_user_id, photo_url) # Assuming profiles.update_photo exists
    return {"photo_url": photo_url}

# Example of how to run for development, if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    # Ensure JWT_SECRET is set in your environment for development
    # e.g., export JWT_SECRET="your_dev_secret_key"
    if not os.getenv("JWT_SECRET"):
        print("Warning: JWT_SECRET environment variable is not set. Using default 'super-secret'.")
        print("For production, set a strong, unique secret key.")

    uvicorn.run(app, host="0.0.0.0", port=8000)