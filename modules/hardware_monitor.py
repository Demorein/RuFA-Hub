import psutil
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface import data_handler
import sql

db = sql.SQL("dbdb.db")

def get_system_info():
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            # Два отдельных запроса
            db.write("settings", data={"key": "CPU", "value": f"{cpu_usage}"})
            db.write("settings", data={"key": "RAM", "value": f"{ram_usage}"})

            # Обновление интерфейса
            data_handler.update_hardware_data()

        except Exception as e:
            db.write("logs", data={"log_message": f"Ошибка в get_system_info: {str(e)}"}, log_level="ERROR")
