# manager.py
import sqlite3

class DBManager:
    def __init__(self, db_name="papeleria.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()

    def fetchall(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetchone(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
