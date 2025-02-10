import sqlite3
import os

class sql_func:
    def __init__(self, db_name):
        
        '''
        Функция котрая проверяет наличие базы данный по названием db_name.\n
        Если такой базы нет, то создаёт новую с название6 bd_name\n
        Создаёт таблицу hosts с столбцами id, ip, port
        '''
        
        self.db_name = db_name
        
        if not os.path.exists(self.db_name):
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
        
        '''
        Проверяет наличие записи с ip port в таблице\n
        Если записей нет, то добавляет ip port в таблицу
        '''
        
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Проверяем, есть ли уже такая запись
        cursor.execute("SELECT COUNT(*) FROM hosts WHERE ip = ? AND port = ?", (ip, port))
        result = cursor.fetchone()

        if result[0] == 0:  # Если записей с таким IP и портом нет
            cursor.execute("INSERT INTO hosts (ip, port) VALUES (?, ?)", (ip, port))
            conn.commit()
            conn.close()
        else:
            conn.close()





    def delete_host(self, ip, port):
        
        '''
        Удаляет запись с ip port
        '''
        
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
        """Удаляет все записи из таблицы"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM hosts")
        conn.commit()
        conn.close()
    