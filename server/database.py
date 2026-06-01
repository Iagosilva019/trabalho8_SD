import sqlite3
from auth import hash_password

DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        username TEXT PRIMARY KEY,
        senha_hash TEXT NOT NULL,
        papel TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente TEXT,
        destinatario TEXT,
        conteudo_cifrado BLOB,
        timestamp TEXT,
        lida INTEGER DEFAULT 0
    )
    """)

    conn.commit()

    cursor.execute("SELECT * FROM usuarios WHERE username='admin'")

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO usuarios VALUES(?,?,?)",
            ("admin", hash_password("admin123"), "admin")
        )

        cursor.execute(
            "INSERT INTO usuarios VALUES(?,?,?)",
            ("joao", hash_password("123456"), "user")
        )

        cursor.execute(
            "INSERT INTO usuarios VALUES(?,?,?)",
            ("maria", hash_password("654321"), "user")
        )

    conn.commit()
    conn.close()
