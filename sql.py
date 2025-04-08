import sqlite3
from datetime import datetime

class SQL:
    def __init__(self, db_name: str):
        self.db_name = db_name


        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS system_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flask_host TEXT,
                    mcis_host TEXT,
                    server_status TEXT
                );

                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    log_level TEXT,
                    message TEXT
                );

                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value TEXT
                );
            """)
            conn.commit()


    def write(self, table_name: str, data: dict, log_level: str = "INFO"):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            if table_name == "logs":
                cursor.execute("""
                    INSERT INTO logs (timestamp, log_level, message)
                    VALUES (?, ?, ?)
                """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log_level, data["log_message"]))

            elif table_name == "settings":
                cursor.execute("""
                    INSERT INTO settings (key, value) 
                    VALUES (?, ?) 
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """, (data["key"], data["value"]))

            elif table_name == "system_status":
                cursor.execute("""
                    INSERT INTO system_status (id, flask_host, mcis_host, server_status) 
                    VALUES (1, ?, ?, ?) 
                    ON CONFLICT(id) DO UPDATE SET 
                        flask_host = excluded.flask_host,
                        mcis_host = excluded.mcis_host,
                        server_status = excluded.server_status
                """, (data["flask_host"], data["mcis_host"], data["server_status"]))

            conn.commit()


        def read(self, table_name: str, key: str = None):
            """Читает данные из указанной таблицы. 
            Для settings можно передать key, чтобы получить конкретное значение.
            """
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                if table_name == "settings" and key:
                    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                    result = cursor.fetchone()
                    return result[0] if result else None

                cursor.execute(f"SELECT * FROM {table_name}")
                return cursor.fetchall()


    def clear_logs(self):
        """Очищает все записи из таблицы logs"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM logs")
        conn.commit()
        conn.close()
