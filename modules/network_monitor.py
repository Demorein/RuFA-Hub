import psutil
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface.data_handler import update_network_data

def get_network_load(max_bandwidth=1000 * 1024 * 1024):

    while True:

        last_net = psutil.net_io_counters()
        last_time = time.time()

        time.sleep(1)

        current_net = psutil.net_io_counters()
        current_time = time.time()

        elapsed_time = current_time - last_time

        download_speed = (current_net.bytes_recv - last_net.bytes_recv) * 8 / elapsed_time  # в битах/с
        upload_speed = (current_net.bytes_sent - last_net.bytes_sent) * 8 / elapsed_time  # в битах/с

        download_load = (download_speed / max_bandwidth) * 100
        upload_load = (upload_speed / max_bandwidth) * 100

        update_network_data({"download": download_load, "upload": upload_load})



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