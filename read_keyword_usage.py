import sqlite3

DB_NAME = 'mandemos.db'


def read_keyword_usage():
    """Print all keyword usage statistics stored in the database."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT clone_id, keyword, count FROM keyword_usage ORDER BY clone_id, keyword')
    rows = cur.fetchall()
    if not rows:
        print('No keyword usage data found.')
    else:
        for clone_id, keyword, count in rows:
            print(f"{clone_id} - {keyword}: {count}")
    conn.close()


if __name__ == '__main__':
    read_keyword_usage()
