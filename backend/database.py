import sqlite3

DB_PATH = "vibevault.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT DEFAULT '',
            badge TEXT DEFAULT 'Explorer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            genre TEXT,
            mood TEXT,
            description TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_collection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER,
            status TEXT DEFAULT 'saved',
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS moodboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            theme_color TEXT DEFAULT '#6C63FF',
            quote TEXT DEFAULT '',
            is_public INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Seed sample items
    c.execute("SELECT COUNT(*) FROM items")
    if c.fetchone()[0] == 0:
        sample_items = [
            ("Interstellar", "film", "Sci-Fi", "Epic", "A journey through space and time"),
            ("Parasite", "film", "Thriller", "Dark", "Class warfare in modern Korea"),
            ("Your Name", "film", "Romance", "Melancholic", "Two strangers connected across time"),
            ("Spirited Away", "film", "Fantasy", "Dreamy", "A girl lost in a spirit world"),
            ("The Dark Knight", "film", "Action", "Intense", "Batman vs The Joker"),
            ("Bohemian Rhapsody", "musik", "Rock", "Energetic", "The story of Queen and Freddie Mercury"),
            ("In the Aeroplane Over the Sea", "musik", "Indie", "Melancholic", "Classic Neutral Milk Hotel album"),
            ("Random Access Memories", "musik", "Electronic", "Groovy", "Daft Punk's iconic album"),
            ("Kind of Blue", "musik", "Jazz", "Chill", "Miles Davis masterpiece"),
            ("Igor", "musik", "R&B", "Dark", "Tyler the Creator's genre-bending album"),
        ]
        c.executemany(
            "INSERT INTO items (title, type, genre, mood, description) VALUES (?,?,?,?,?)",
            sample_items
        )

    conn.commit()
    conn.close()
