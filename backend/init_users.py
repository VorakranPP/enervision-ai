import sqlite3
from pathlib import Path
from passlib.context import CryptContext

DB_PATH = Path(__file__).resolve().parent / "energy_data.db"
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
    password TEXT,
    role TEXT DEFAULT 'viewer'
)
""")

admin_password = pwd_context.hash("admin123")

cursor.execute("""
INSERT OR REPLACE INTO users (username, password, role)
VALUES (?, ?, ?)
""", ("admin", admin_password, "admin"))

demo_password = pwd_context.hash("Demo123!")

cursor.execute("""
INSERT OR REPLACE INTO users (username, password, role)
VALUES (?, ?, ?)
""", ("demo@enervision.ai", demo_password, "viewer"))

connection.commit()
connection.close()

print("✅ users table ready")
print("✅ admin user created    — admin / admin123")
print("✅ demo account created  — demo@enervision.ai / Demo123!")