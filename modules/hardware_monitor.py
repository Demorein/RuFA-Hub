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