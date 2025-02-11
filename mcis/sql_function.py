import sqlite3
from os import path

class sql_func:
    def __init__(self, db_name):
        self.db_name = db_name
        
        if not path.exists(self.db_name):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
        
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hosts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    api TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()

    def insert_host(self, ip, port, api):  
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM hosts WHERE ip = ? AND port = ?", (ip, port))
        result = cursor.fetchone()

        if result[0] == 0:
            cursor.execute("INSERT INTO hosts (ip, port, api) VALUES (?, ?, ?)", (ip, port, api))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    def delete_host(self, ip, port):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM hosts WHERE ip = ? AND port = ?", (ip, port))
        result = cursor.fetchone()

        if result[0] > 0:
            cursor.execute("DELETE FROM hosts WHERE ip = ? AND port = ?", (ip, port))
            conn.commit()
        
        conn.close()

    def delete_all_hosts(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM hosts")
        conn.commit()
        conn.close()

    def show_all_hosts(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM hosts")
        rows = cursor.fetchall()
        
        conn.close()

        if not rows:
            return "В таблице нет данных."

        result = []
        for row in rows:
            result.append(f"id: {row[0]}, ip: {row[1]}, port: {row[2]}, api: {row[3]}")
        
        return "\n".join(result)
