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
                port INTEGER NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()

            
            
    def insert_host(self, ip, port):  
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM hosts WHERE ip = ? AND port = ?", (ip, port))
        result = cursor.fetchone()

        if result[0] == 0:
            cursor.execute("INSERT INTO hosts (ip, port) VALUES (?, ?)", (ip, port))
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
        else:
            conn.close()




    def delete_all_hosts(self):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM hosts")
        conn.commit()
        conn.close()
    