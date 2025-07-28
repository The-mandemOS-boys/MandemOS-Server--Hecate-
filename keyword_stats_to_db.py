import os
import sqlite3
import requests

DB_NAME = 'mandemos.db'
SERVER_URL = os.getenv('CLONE_SERVER_URL', 'http://localhost:5000')


def init_db():
    """Ensure the keyword_usage table exists and return connection."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS keyword_usage (
            clone_id TEXT,
            keyword TEXT,
            count INTEGER,
            PRIMARY KEY (clone_id, keyword)
        )'''
    )
    conn.commit()
    return conn


def fetch_keyword_stats():
    """Retrieve keyword usage stats from the clone network server."""
    resp = requests.get(f"{SERVER_URL}/keywords", timeout=5)
    resp.raise_for_status()
    return resp.json()


def store_stats(conn, stats):
    cur = conn.cursor()
    for clone_id, keywords in stats.items():
        for kw, count in keywords.items():
            cur.execute(
                'INSERT OR REPLACE INTO keyword_usage (clone_id, keyword, count) VALUES (?, ?, ?)',
                (clone_id, kw, count)
            )
    conn.commit()


def main():
    conn = init_db()
    stats = fetch_keyword_stats()
    store_stats(conn, stats)
    conn.close()
    print('Keyword usage stored to database')


if __name__ == '__main__':
    main()
