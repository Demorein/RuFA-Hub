import sqlite3
from os import path

#SQL

class sql_func:
    def __init__(self, db_name):
        self.db_name = db_name
        
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

    def get_api_by_ip(self, ip):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT api FROM hosts WHERE ip = ?", (ip,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]  # Возвращаем API-ключ
        else:
            return None  # Если IP не найден
        



# RuFA-Hub
# Copyright (C) 2025 Gromov Evgeniy Vyacheslavovich

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 2 for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
