# models/bmi_model.py

import sqlite3
from datetime import datetime
import hashlib
import os
from contextlib import contextmanager

class BMIModel:
    def __init__(self, db_name="bmi_data.db"):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password BLOB
                )
            """)
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    age INTEGER,
                    height REAL,
                    weight REAL,
                    bmi REAL,
                    category TEXT,
                    calculated_at TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            conn.commit()

    def hash_password(self, password, salt=None):
        if not salt:
            salt = os.urandom(16)  # 16 bytes salt
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt + pwd_hash  # Store salt + hash together

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:16]
        stored_hash = stored_password[16:]
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
        return pwd_hash == stored_hash

    def register_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                hashed_password = self.hash_password(password)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def login_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and self.verify_password(user[1], password):
                return user[0]
            return None

    def save_bmi(self, user_id, age, height, weight, bmi, category):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_records (user_id, age, height, weight, bmi, category, calculated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, age, height, weight, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def get_history(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bmi_records WHERE user_id = ? ORDER BY calculated_at DESC", (user_id,))
            records = cursor.fetchall()
            return records

    def delete_record(self, record_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bmi_records WHERE id = ?", (record_id,))
            conn.commit()

    @staticmethod
    def calculate_bmi(height, weight):
        if height <= 0 or weight <= 0:
            raise ValueError("Chiều cao và cân nặng phải lớn hơn 0.")
        bmi = weight / (height ** 2)
        if bmi < 16:
            category = "Cực kỳ nhẹ cân"
        elif 16 <= bmi < 17:
            category = "Rất nhẹ cân"
        elif 17 <= bmi < 18.5:
            category = "Nhẹ cân"
        elif 18.5 <= bmi < 25:
            category = "Bình thường"
        elif 25 <= bmi < 30:
            category = "Thừa cân"
        elif 30 <= bmi < 35:
            category = "Béo phì (Loại I)"
        elif 35 <= bmi < 40:
            category = "Béo phì (Loại II)"
        else:
            category = "Béo phì (Loại III)"
        return bmi, category
