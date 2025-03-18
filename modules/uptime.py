import psutil
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface import data_handler

def uptime_parcer():
    while True:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
        h, m = uptime_str.replace("h", "").replace("m", "").split()
        a = {"h": f"{h}h", "m": f"{m}m"}
        data_handler.update_uptime_data(a)
