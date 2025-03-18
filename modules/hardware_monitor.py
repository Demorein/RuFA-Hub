import psutil
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface import data_handler


def get_system_info():
    while True:
        time.sleep(0.1)
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_info = psutil.virtual_memory()
        ram_usage = ram_info.percent

        data = {
            "CPU": f"{cpu_usage}",
            "RAM": f"{ram_usage}"
        }

        data_handler.update_hardware_data(data)
        
