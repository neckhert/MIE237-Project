import sqlite3

def connect_db(db_name='voting_data.db'):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            video_id TEXT NOT NULL,
            vote INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def insert_vote(conn, user_id, video_id, vote):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO votes (user_id, video_id, vote)
        VALUES (?, ?, ?)
    ''', (user_id, video_id, vote))
    conn.commit()

def fetch_votes(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM votes')
    return cursor.fetchall()

def close_db(conn):
    conn.close()