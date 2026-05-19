import sqlite3
from pathlib import Path
from passlib.context import CryptContext

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy_data.db"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    hashed_password TEXT,
    role TEXT DEFAULT 'viewer'
)
""")

hashed_password = pwd_context.hash("admin123")

cursor.execute("""
INSERT OR IGNORE INTO users (
    username,
    hashed_password,
    role
)
VALUES (?,?,?)
""", (
(
"admin",
hashed_password,
"admin"
)
))

connection.commit()
connection.close()

print("User created")