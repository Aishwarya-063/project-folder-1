# DAL.py
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

_DB_PATH = Path(__file__).with_name("projects.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row  # return dict-like rows
    return conn


def init_db() -> None:
    """
    Creates the projects.db file and the projects table if they don't exist.
    """
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT NOT NULL,
                ImageFileName TEXT NOT NULL,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


def get_all_projects() -> List[Dict[str, Any]]:
    """
    Returns all projects ordered by newest first.
    """
    with _connect() as conn:
        cur = conn.execute(
            "SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects ORDER BY CreatedAt DESC, id DESC;"
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def count_projects() -> int:
    with _connect() as conn:
        cur = conn.execute("SELECT COUNT(*) AS c FROM projects;")
        return int(cur.fetchone()["c"])


def insert_project(title: str, description: str, image_file_name: str) -> int:
    """
    Inserts a project and returns the new row id.
    """
    if not title.strip() or not description.strip() or not image_file_name.strip():
        raise ValueError("Title, Description, and Image file name are required.")

    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO projects (Title, Description, ImageFileName) VALUES (?, ?, ?);",
            (title.strip(), description.strip(), image_file_name.strip()),
        )
        conn.commit()
        return cur.lastrowid
