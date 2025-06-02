import psutil
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface import data_handler

def uptime_parcer():
    while True:
        time.sleep(50)
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
        h, m = uptime_str.replace("h", "").replace("m", "").split()
        a = {"h": f"{h}h", "m": f"{m}m"}
        data_handler.update_uptime_data(a)


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