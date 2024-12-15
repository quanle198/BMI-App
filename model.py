import sqlite3
from datetime import datetime

class BMIModel:
    def __init__(self, db_name="bmi_data.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
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
        conn.close()

    def register_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        print(username)
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None

    def save_bmi(self, user_id, age, height, weight, bmi, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO bmi_records (user_id, age, height, weight, bmi, category, calculated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, age, height, weight, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def get_history(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bmi_records WHERE user_id = ? ORDER BY calculated_at DESC", (user_id,))
        records = cursor.fetchall()
        conn.close()
        return records

    def delete_record(self, record_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bmi_records WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()

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
