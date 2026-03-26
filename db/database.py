import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = "./database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                last_login  TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                role        TEXT NOT NULL,
                content     TEXT NOT NULL,
                timestamp   TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      TEXT NOT NULL,
                filename     TEXT NOT NULL,
                filetype     TEXT NOT NULL,
                uploaded_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT NOT NULL,
                query       TEXT NOT NULL,
                timestamp   TEXT NOT NULL
            )
        """)
        conn.commit()

def save_message(role: str, content: str):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute(
            "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, datetime.now().isoformat())
        )
        conn.commit()

def save_file(user_id: str, filename: str, filetype: str):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute(
            "INSERT INTO files (user_id, filename, filetype, uploaded_at) VALUES (?, ?, ?, ?)",
            (user_id, filename, filetype, datetime.now().isoformat())
        )
        conn.commit()

def save_search(user_id: str, query: str):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute(
            "INSERT INTO searches (user_id, query, timestamp) VALUES (?, ?, ?)",
            (user_id, query, datetime.now().isoformat())
        )
        conn.commit()