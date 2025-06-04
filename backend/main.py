from __future__ import annotations

import os
import sqlite3
from datetime import time, date
from fastapi import FastAPI, HTTPException, Request, Depends, Header, Response
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt as jose_jwt
from pathlib import Path
from uuid import uuid4

import logging
from pydantic import BaseModel

from src import (
    auth,
    mindful,
    dashboard,
    relationships,
    activity,
    notifications,
    subscriptions,
    challenges,
    sessions as session_models,
    profiles,
    analytics,
    ads,
)
from src import monitoring
from src.api_models import (
    DateValuePoint,
    ConsistencyDataResponse,
    MoodCorrelationPoint,
    MoodCorrelationResponse,
    HourValuePoint,
    TimeOfDayResponse,
    StringValuePoint,
    LocationFrequencyResponse,
    AdResponse,
    CustomTypeInput,
    CustomTypeResponse,
    ProfileVisibilityInput,
    BadgeResponse,
    PrivateChallengeInput,
    PrivateChallengeResponse,
    PublicProfileResponse,
)
from src.feed_models import (
    CommentInput,
    EncouragementInput,
    FeedInteractionResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mindful")

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret")  # Changed default for clarity
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
    logger.info(
        "Completed %s %s %s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


# Assuming ActivityFeed and NotificationManager classes were updated to accept 'conn'
feed = activity.ActivityFeed(conn)
notify_manager = notifications.NotificationManager(conn)
ad_manager = ads.AdManager(conn)


def get_current_user(authorization: str = Header(None)) -> int:
    """Return the authenticated user's ID from a Bearer token."""
    # ``Authorization`` header should look like ``Bearer <token>``.
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated: Missing token")

    token = authorization.split(" ", 1)[1]
    try:
        # Decode and validate the JWT. ``SECRET_KEY`` and ``ALGORITHM`` must
        # match the values used when the token was created.
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")
        if user_id_from_token is None:
            # ``user_id`` is a custom claim we expect to always be present.
            raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id_from_token)


def get_optional_user(authorization: str = Header(None)) -> int | None:
    """Return the user ID if a valid Bearer token is provided, else ``None``."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")
        if user_id_from_token is None:
            return None
        return int(user_id_from_token)
    except JWTError:
        return None


def _get_user_sessions_with_moods(user_id: int) -> list[session_models.MeditationSession]:
    """Return all sessions for the user including mood data."""
    cur = conn.execute(
        "SELECT s.duration, s.session_type, s.session_date, s.session_time, s.location, m.mood_before, m.mood_after "
        "FROM sessions s LEFT JOIN moods m ON s.id = m.session_id WHERE s.user_id = ?",
        (user_id,),
    )
    rows = cur.fetchall()
    return [
        session_models.MeditationSession(
            duration_minutes=r[0],
            meditation_type=r[1],
            session_date=date.fromisoformat(r[2]) if isinstance(r[2], str) else r[2],
            time_of_day=time.fromisoformat(r[3]) if r[3] else time(0, 0),
            location=r[4] or "",
            mood_before=r[5],
            mood_after=r[6],
        )
        for r in rows
    ]


class SignUp(BaseModel):
    email: str
    password: str
    display_name: str | None = None


class Login(BaseModel):
    email: str
    password: str


class SocialLoginInput(BaseModel):
    """Access token obtained from a third-party auth provider."""

    provider: str
    token: str


class SessionInput(BaseModel):
    date: str  # Expect ISO format string e.g. "YYYY-MM-DD"
    time: str | None = None  # Expect ISO format string e.g. "HH:MM" or "HH:MM:SS"
    duration: int
    type: str
    location: str | None = None
    notes: str | None = None
    moodBefore: int | None = None
    moodAfter: int | None = None


class FollowInput(BaseModel):
    followed_id: int


class NotificationInput(BaseModel):
    reminder_time: str  # Expect ISO format string e.g. "HH:MM" or "HH:MM:SS"
    message: str
    enabled: bool = True  # Added from one of the versions


class BioUpdate(BaseModel):
    bio: str


class PrivateChallengeInput(BaseModel):
    name: str
    target_minutes: int
    start_date: str
    end_date: str


# Removed redundant BioUpdate class definition that was present in the conflict


@app.post("/auth/signup")
def signup_user(data: SignUp):  # Renamed for clarity from just 'signup'
    user_id = auth.register_user(
        conn, data.email, data.password, display_name=data.display_name
    )
    monitoring.log_event("signup", {"user": user_id})
    return {"user_id": user_id}


@app.post("/auth/login")
def login_user(data: Login):  # Renamed for clarity
    cur = conn.execute(
        "SELECT id, password_hash FROM users WHERE email = ?", (data.email,)
    )
    row = cur.fetchone()
    if not row or row[1] is None or not auth.verify_password(data.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = row[0]
    monitoring.log_event("login", {"user": user_id})
    token_payload = {"user_id": user_id}
    token = jose_jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}  # Added token_type


@app.post("/auth/social-login")
def social_login(data: SocialLoginInput):
    """Log in or register a user via a social provider."""
    try:
        provider_user_id, email = data.token.split(":", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    cur = conn.execute(
        "SELECT user_id FROM social_accounts WHERE provider = ? AND provider_user_id = ?",
        (data.provider, provider_user_id),
    )
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        user_id = auth.register_social_user(
            conn, data.provider, provider_user_id, email=email
        )

    monitoring.log_event(
        "social_login", {"user": user_id, "provider": data.provider}
    )
    token_payload = {"user_id": user_id}
    token = jose_jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/sessions", response_model=dict)  # Added response_model
def create_session(
    info: SessionInput, current_user_id: int = Depends(get_current_user)
):
    session_id = mindful.log_session(
        conn,
        current_user_id,  # Use current_user_id from token
        info.duration,
        info.type,
        info.date,
        session_time=info.time,
        location=info.location,
        notes=info.notes,
        mood_before=info.moodBefore,
        mood_after=info.moodAfter,
    )
    feed.log_session(current_user_id, f"{info.type} {info.duration}m")
    cur = conn.execute(
        "SELECT COUNT(*) FROM sessions WHERE user_id = ?",
        (current_user_id,),
    )
    count = cur.fetchone()[0]
    if count == 1:
        challenges.award_badge(conn, current_user_id, "First Session Completed")
    return {"session_id": session_id}


@app.get("/dashboard/me", response_model=dict)
def get_dashboard_data(current_user_id: int = Depends(get_current_user)):
    cur = conn.execute(
        "SELECT duration, session_type, session_date, session_time, location, photo_url FROM sessions WHERE user_id = ?",
        (current_user_id,),
    )
    records = cur.fetchall()
    sess = [
        session_models.MeditationSession(
            duration_minutes=r[0],
            meditation_type=r[1],
            time_of_day=time.fromisoformat(r[3]) if r[3] else time(0, 0),
            # Ensure r[2] (session_date) is a date object or string that can be parsed
            session_date=date.fromisoformat(r[2]) if isinstance(r[2], str) else r[2],
            location=r[4] or "",
            photo_url=r[5],
        )
        for r in records
    ]
    total = dashboard.calculate_total_time(sess)
    count = dashboard.calculate_session_count(sess)
    streak = dashboard.calculate_current_streak(sess)
    return {
        "total": total,
        "sessions": count,
        "streak": streak,
    }

@app.get("/feed", response_model=list)  # Changed path to /feed, user_id from token
def get_user_feed(current_user_id: int = Depends(get_current_user)):
    # This is the implementation from the third provided diff for /feed
    followed_ids = relationships.get_following(conn, current_user_id)
    # User should also see their own items in their feed
    user_ids_for_feed = set(followed_ids)
    user_ids_for_feed.add(current_user_id)

    if not user_ids_for_feed:
        return []

    # Build a dynamic placeholder string (?,?,?) for the ``IN`` clause based on
    # how many user ids we're querying for. SQLite requires ``?`` for each value.
    placeholders = ",".join("?" for _ in user_ids_for_feed)

    # ``activity_feed`` table stores all social feed items. Ensure the query
    # matches the schema defined in scripts/init_db.sql and ActivityFeed.
    query = (
        "SELECT f.id, f.user_id, u.display_name, f.item_type, f.message, f.timestamp, f.target_user_id, f.related_feed_item_id "
        "FROM activity_feed f JOIN users u ON f.user_id = u.id "
        f"WHERE f.user_id IN ({placeholders}) AND (u.is_public = 1 OR f.user_id = ?) "
        "ORDER BY f.timestamp DESC, f.id DESC LIMIT 20"
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
                "timestamp": (
                    r[5].isoformat() if isinstance(r[5], (date, time)) else r[5]
                ),  # Ensure ISO format
                "target_user_id": r[6],
                "related_feed_item_id": r[7],
            }
            for r in rows
        ]


@app.post("/feed/{feed_item_id}/comment", response_model=FeedInteractionResponse)
def comment_on_feed_item(
    feed_item_id: int,
    data: CommentInput,
    current_user_id: int = Depends(get_current_user),
):
    """Add a comment to a feed item."""
    # Ensure the request body feed_item_id matches the URL parameter
    if data.feed_item_id != feed_item_id:
        raise HTTPException(status_code=400, detail="Mismatched feed_item_id")

    cur = conn.execute(
        "SELECT user_id FROM activity_feed WHERE id = ?",
        (feed_item_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Feed item not found")
    target_user_id = row[0]
    interaction_id = feed.add_comment(
        current_user_id,
        target_user_id,
        data.text,
        related_feed_item_id=feed_item_id,
    )
    return FeedInteractionResponse(
        interaction_id=interaction_id, message="Comment added"
    )


@app.post("/feed/{feed_item_id}/encourage", response_model=FeedInteractionResponse)
def encourage_feed_item(
    feed_item_id: int,
    data: EncouragementInput,
    current_user_id: int = Depends(get_current_user),
):
    """Send encouragement related to a feed item."""
    if data.feed_item_id != feed_item_id:
        raise HTTPException(status_code=400, detail="Mismatched feed_item_id")

    cur = conn.execute(
        "SELECT user_id FROM activity_feed WHERE id = ?",
        (feed_item_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Feed item not found")
    target_user_id = row[0]
    interaction_id = feed.add_encouragement(
        current_user_id,
        target_user_id,
        data.text,
        related_feed_item_id=feed_item_id,
    )
    return FeedInteractionResponse(
        interaction_id=interaction_id, message="Encouragement sent"
    )


@app.post("/follow", response_model=dict)
def follow_user_action(
    data: FollowInput, current_user_id: int = Depends(get_current_user)
):  # Renamed
    if current_user_id == data.followed_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    relationships.follow_user(conn, current_user_id, data.followed_id)
    return {
        "status": "ok",
        "message": f"User {current_user_id} now follows {data.followed_id}",
    }


@app.post("/unfollow", response_model=dict)
def unfollow_user_action(
    data: FollowInput, current_user_id: int = Depends(get_current_user)
):  # Renamed
    relationships.unfollow_user(conn, current_user_id, data.followed_id)
    return {
        "status": "ok",
        "message": f"User {current_user_id} unfollowed {data.followed_id}",
    }


@app.post("/notifications", response_model=dict)
def add_user_notification(
    data: NotificationInput, current_user_id: int = Depends(get_current_user)
):  # Renamed
    try:
        reminder_time_obj = time.fromisoformat(data.reminder_time)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid reminder_time format. Use HH:MM or HH:MM:SS.",
        )
    note_id = notify_manager.add_notification(
        current_user_id, reminder_time_obj, data.message, data.enabled
    )
    return {"notification_id": note_id}


@app.get("/notifications", response_model=list)  # Changed path, user_id from token
def list_user_notifications(
    current_user_id: int = Depends(get_current_user),
):  # Renamed
    notes = notify_manager.get_notifications(current_user_id)
    return [
        n.dict() if hasattr(n, "dict") else n.__dict__ for n in notes
    ]  # Use .dict() if Pydantic model


class JoinChallengeInput(BaseModel):
    challenge_id: int


@app.get("/challenges", response_model=list)  # Added response_model
def list_community_challenges():  # Renamed
    cur = conn.execute(
        "SELECT id, name, target_minutes, start_date, end_date FROM community_challenges"
    )
    rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "target_minutes": r[2],
            "start_date": (
                r[3].isoformat() if isinstance(r[3], date) else r[3]
            ),  # Ensure ISO format
            "end_date": (
                r[4].isoformat() if isinstance(r[4], date) else r[4]
            ),  # Ensure ISO format
        }
        for r in rows
    ]


@app.post("/challenges/join", response_model=dict)  # Added response_model
def join_community_challenge(
    data: JoinChallengeInput, current_user_id: int = Depends(get_current_user)
):  # Renamed
    mindful.join_challenge(conn, current_user_id, data.challenge_id)
    return {
        "status": "ok",
        "message": f"User {current_user_id} joined challenge {data.challenge_id}",
    }


@app.get("/moods", response_model=list)  # Changed path, user_id from token
def get_user_moods(current_user_id: int = Depends(get_current_user)):  # Renamed
    moods = mindful.get_user_moods(conn, current_user_id)
    return [{"before": m[0], "after": m[1]} for m in moods]


class SubscriptionUpdate(BaseModel):
    tier: str


@app.get("/subscriptions/me", response_model=dict)  # Changed path for current user
def get_my_subscription(current_user_id: int = Depends(get_current_user)):  # Renamed
    tier = subscriptions.get_user_tier(conn, current_user_id)
    return {"tier": tier}


@app.put(
    "/subscriptions/me", response_model=dict
)  # Changed to PUT, path for current user
def update_my_subscription(
    data: SubscriptionUpdate, current_user_id: int = Depends(get_current_user)
):  # Renamed
    # Assuming start_date is current date or handled by subscribe_user
    subscriptions.subscribe_user(
        conn, current_user_id, data.tier, date.today().isoformat()
    )
    return {"status": "ok", "tier": data.tier}


@app.put("/users/me/bio", response_model=dict)  # Path for current user
def update_my_bio(
    data: BioUpdate, current_user_id: int = Depends(get_current_user)
):  # Renamed
    profiles.update_bio(
        conn, current_user_id, data.bio
    )  # Assuming profiles.update_bio exists
    return {"status": "ok", "message": "Bio updated successfully."}


@app.post("/users/me/photo", response_model=dict)  # Path for current user
async def upload_my_photo(
    request: Request, current_user_id: int = Depends(get_current_user)
):  # Renamed
    content_type = request.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid content type, please upload an image."
        )

    file_data = await request.body()
    if not file_data:
        raise HTTPException(status_code=400, detail="No image data received.")

    # Generate a file name using a client provided name if available. This
    # keeps a hint of the original extension while avoiding collisions.
    original_filename = request.headers.get("X-Filename", f"photo_{current_user_id}")
    ext = Path(original_filename).suffix or ".jpg"  # Default to .jpg if no extension
    if ext.lower() not in [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]:  # Basic extension validation
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please use JPG, PNG, or GIF.",
        )

    # Use a random UUID to avoid overwriting existing files with the same name.
    filename = f"{uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    try:
        with open(dest, "wb") as out_file:
            out_file.write(file_data)
    except IOError:
        logger.error(f"IOError saving uploaded photo to {dest}")
        raise HTTPException(status_code=500, detail="Could not save uploaded photo.")

    photo_url = f"/uploads/{filename}"
    profiles.update_photo(
        conn, current_user_id, photo_url
    )  # Assuming profiles.update_photo exists
    return {"photo_url": photo_url}


@app.put("/users/me/profile-visibility", response_model=dict)
def update_profile_visibility(
    data: ProfileVisibilityInput, current_user_id: int = Depends(get_current_user)
):
    """Update whether the authenticated user's profile is public."""
    profiles.update_visibility(conn, current_user_id, data.is_public)
    return {"status": "ok"}


@app.get("/users/{user_id}/profile", response_model=PublicProfileResponse)
def get_user_profile(
    user_id: int, requester_id: int | None = Depends(get_optional_user)
):
    """Return public profile information for ``user_id``."""
    try:
        profile = profiles.get_profile_with_stats(conn, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

    if not profile["is_public"] and requester_id != user_id:
        raise HTTPException(status_code=403, detail="Profile is private")

    return PublicProfileResponse(
        user_id=profile["user_id"],
        display_name=profile["display_name"],
        bio=profile["bio"],
        photo_url=profile["photo_url"],
        total_minutes=profile["total_minutes"],
        session_count=profile["session_count"],
    )

@app.get("/users/me/custom-meditation-types", response_model=list)
def list_custom_types(current_user_id: int = Depends(get_current_user)):
    cur = conn.execute(
        "SELECT id, type_name FROM custom_meditation_types WHERE user_id = ?",
        (current_user_id,),
    )
    return [{"id": r[0], "type_name": r[1]} for r in cur.fetchall()]


@app.post("/users/me/custom-meditation-types", response_model=dict)
def create_custom_type(
    data: CustomTypeInput, current_user_id: int = Depends(get_current_user)
):
    new_id = uuid4().hex
    conn.execute(
        "INSERT INTO custom_meditation_types (id, user_id, type_name) VALUES (?, ?, ?)",
        (new_id, current_user_id, data.type_name),
    )
    conn.commit()
    return {"id": new_id, "type_name": data.type_name}


@app.put("/users/me/custom-meditation-types/{type_id}", response_model=dict)

def update_custom_type(
    type_id: str,
    data: CustomTypeInput,
    current_user_id: int = Depends(get_current_user),
):
    conn.execute(
        "UPDATE custom_meditation_types SET type_name = ? WHERE id = ? AND user_id = ?",
        (data.type_name, type_id, current_user_id),
    )
    conn.commit()
    return {"status": "ok"}


@app.delete("/users/me/custom-meditation-types/{type_id}", response_model=dict)
def delete_custom_type(type_id: str, current_user_id: int = Depends(get_current_user)):
    conn.execute(
        "DELETE FROM custom_meditation_types WHERE id = ? AND user_id = ?",
        (type_id, current_user_id),
    )
    conn.commit()
    return {"status": "deleted"}


@app.get("/users/me/badges", response_model=list)
def list_badges(current_user_id: int = Depends(get_current_user)):
    cur = conn.execute(
        "SELECT badge_name FROM badges WHERE user_id = ? ORDER BY awarded_at",
        (current_user_id,),
    )
    return [{"name": r[0]} for r in cur.fetchall()]


@app.get("/users/me/private-challenges", response_model=list)
def list_private_challenges(current_user_id: int = Depends(get_current_user)):
    cur = conn.execute(
        "SELECT id, name FROM challenges WHERE created_by = ? AND is_private = 1",
        (current_user_id,),
    )
    return [{"id": r[0], "name": r[1]} for r in cur.fetchall()]


@app.post("/users/me/private-challenges", response_model=dict)

def create_private_challenge(
    data: PrivateChallengeInput, current_user_id: int = Depends(get_current_user)
):
    if not subscriptions.is_premium(conn, current_user_id):
        raise HTTPException(status_code=403, detail="Premium subscription required")
    cur = conn.execute(
        "INSERT INTO challenges (name, created_by, is_private) VALUES (?, ?, 1) RETURNING id",
        (data.name, current_user_id),
    )
    challenge_id = cur.fetchone()[0]
    conn.commit()
    return {"id": challenge_id, "name": data.name}


@app.put("/users/me/private-challenges/{challenge_id}", response_model=dict)

def update_private_challenge(
    challenge_id: int,
    data: PrivateChallengeInput,
    current_user_id: int = Depends(get_current_user),
):
    if not subscriptions.is_premium(conn, current_user_id):
        raise HTTPException(status_code=403, detail="Premium subscription required")
    conn.execute(
        "UPDATE challenges SET name = ? WHERE id = ? AND created_by = ? AND is_private = 1",
        (data.name, challenge_id, current_user_id),
    )
    conn.commit()
    return {"status": "ok"}


@app.delete("/users/me/private-challenges/{challenge_id}", response_model=dict)
def delete_private_challenge(
    challenge_id: int, current_user_id: int = Depends(get_current_user)
):
    if not subscriptions.is_premium(conn, current_user_id):
        raise HTTPException(status_code=403, detail="Premium subscription required")
    conn.execute(
        "DELETE FROM challenges WHERE id = ? AND created_by = ? AND is_private = 1",
        (challenge_id, current_user_id),
    )
    conn.commit()
    return {"status": "deleted"}

@app.get("/ads/random", response_model=AdResponse, responses={204: {"description": "No ad available"}})
def get_random_ad() -> AdResponse | Response:
    """Return a random advertisement for free-tier users."""
    try:
        ad = ad_manager.get_random_ad()
    except ValueError:
        return Response(status_code=204)
    return AdResponse(ad_id=ad.ad_id, text=ad.text)


@app.get("/analytics/me/consistency", response_model=ConsistencyDataResponse)
def analytics_consistency(current_user_id: int = Depends(get_current_user)) -> ConsistencyDataResponse:
    sessions = _get_user_sessions_with_moods(current_user_id)
    data = analytics.consistency_over_time(sessions)
    points = [DateValuePoint(date_str=d.isoformat(), value=v) for d, v in data.items()]
    return ConsistencyDataResponse(points=points)


@app.get("/analytics/me/mood-correlation", response_model=MoodCorrelationResponse)
def analytics_mood_correlation(current_user_id: int = Depends(get_current_user)) -> MoodCorrelationResponse:
    sessions = _get_user_sessions_with_moods(current_user_id)
    pairs = analytics.mood_correlation_points(sessions)
    points = [MoodCorrelationPoint(mood_before=p[0], mood_after=p[1]) for p in pairs]
    return MoodCorrelationResponse(points=points)


@app.get("/analytics/me/time-of-day", response_model=TimeOfDayResponse)
def analytics_time_of_day(current_user_id: int = Depends(get_current_user)) -> TimeOfDayResponse:
    sessions = _get_user_sessions_with_moods(current_user_id)
    data = analytics.time_of_day_distribution(sessions)
    points = [HourValuePoint(hour=h, value=v) for h, v in data.items()]
    return TimeOfDayResponse(points=points)


@app.get("/analytics/me/location-frequency", response_model=LocationFrequencyResponse)
def analytics_location_frequency(current_user_id: int = Depends(get_current_user)) -> LocationFrequencyResponse:
    sessions = _get_user_sessions_with_moods(current_user_id)
    data = analytics.location_frequency(sessions)
    points = [StringValuePoint(name=k, value=v) for k, v in data.items()]
    return LocationFrequencyResponse(points=points)


@app.post("/sessions/{session_id}/photo", response_model=dict)
async def upload_session_photo(
    session_id: int,
    request: Request,
    current_user_id: int = Depends(get_current_user),
):
    content_type = request.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid content type, please upload an image."
        )

    cur = conn.execute(
        "SELECT user_id FROM sessions WHERE id = ?",
        (session_id,),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    if row[0] != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this session")

    file_data = await request.body()
    if not file_data:
        raise HTTPException(status_code=400, detail="No image data received.")

    original_filename = request.headers.get("X-Filename", f"session_{session_id}")
    ext = Path(original_filename).suffix or ".jpg"
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please use JPG, PNG, or GIF.",
        )

    filename = f"{uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    try:
        with open(dest, "wb") as out_file:
            out_file.write(file_data)
    except IOError:
        logger.error(f"IOError saving uploaded session photo to {dest}")
        raise HTTPException(status_code=500, detail="Could not save uploaded photo.")

    photo_url = f"/uploads/{filename}"
    conn.execute(
        "UPDATE sessions SET photo_url = ? WHERE id = ?",
        (photo_url, session_id),
    )
    conn.commit()
    return {"photo_url": photo_url}


# Example of how to run for development, if this file is executed directly
if __name__ == "__main__":
    import uvicorn

    # Ensure JWT_SECRET is set in your environment for development
    # e.g., export JWT_SECRET="your_dev_secret_key"
    if not os.getenv("JWT_SECRET"):
        print(
            "Warning: JWT_SECRET environment variable is not set. Using default 'super-secret'."
        )
        print("For production, set a strong, unique secret key.")

    uvicorn.run(app, host="0.0.0.0", port=8000)
