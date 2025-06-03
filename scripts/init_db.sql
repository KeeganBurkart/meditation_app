-- Initial Mindful Connect database schema
-- This script creates tables for users, sessions, and moods.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    session_date DATE NOT NULL,
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
