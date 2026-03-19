import sqlite3
import hashlib
import os
from datetime import datetime
DB_PATH = "./database.db"
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            last_login  TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            role        TEXT NOT NULL,
            content     TEXT NOT NULL,
            timestamp   TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            filename     TEXT NOT NULL,
            filetype     TEXT NOT NULL,
            uploaded_at  TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            query       TEXT NOT NULL,
            timestamp   TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
def save_message(role : str , content : str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (role , content , timestamp) VALUES (?,?,?)",
        (role , content ,datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
def save_file(user_id: str, filename: str, filetype: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO files (user_id, filename, filetype, uploaded_at) VALUES (?, ?, ?, ?)",
        (user_id, filename, filetype, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
def save_search( query : str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO searches (query , timestamp) VALUES (? , ?)",
        (query , datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
init_db()
