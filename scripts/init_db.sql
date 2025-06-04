-- Initial Mindful Connect database schema
-- This script creates tables for users, sessions, moods,
-- and custom meditation types.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    display_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    bio TEXT,
    photo_url TEXT,
    is_public INTEGER DEFAULT 1
);

-- Optional social login providers for each user
CREATE TABLE IF NOT EXISTS social_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    provider_user_id TEXT NOT NULL,
    UNIQUE(provider, provider_user_id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    session_date DATE NOT NULL,
    session_time TEXT,
    location TEXT,
    photo_url TEXT,
    notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    mood_before INTEGER,
    mood_after INTEGER,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS custom_meditation_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type_name TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Table to store earned badges for each user
CREATE TABLE IF NOT EXISTS badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    badge_name TEXT NOT NULL,
    awarded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Challenges optionally allow private visibility
CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_by INTEGER NOT NULL,
    is_private INTEGER DEFAULT 0,
    FOREIGN KEY(created_by) REFERENCES users(id)
);

-- Table to store follow relationships between users
CREATE TABLE IF NOT EXISTS follows (
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY(follower_id) REFERENCES users(id),
    FOREIGN KEY(followed_id) REFERENCES users(id)
);



-- Subscription tiers
CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER PRIMARY KEY,
    tier TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Community challenges for shared meditation goals
CREATE TABLE IF NOT EXISTS community_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_minutes INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- Track progress for users participating in community challenges
CREATE TABLE IF NOT EXISTS challenge_progress (
    user_id INTEGER NOT NULL,
    challenge_id INTEGER NOT NULL,
    minutes INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, challenge_id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(challenge_id) REFERENCES community_challenges(id)
);

-- User configurable notification reminders
CREATE TABLE IF NOT EXISTS user_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reminder_time DATETIME NOT NULL,
    message TEXT,
    is_enabled INTEGER DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Social activity feed items
CREATE TABLE IF NOT EXISTS activity_feed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_type TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    target_user_id INTEGER,
    related_session_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(target_user_id) REFERENCES users(id),
    FOREIGN KEY(related_session_id) REFERENCES sessions(id)
);
  
-- Advertisements for in-app promotions or announcements
CREATE TABLE IF NOT EXISTS advertisements (
    ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);
