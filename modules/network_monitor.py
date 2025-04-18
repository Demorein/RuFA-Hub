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

        download_load = (current_net.bytes_recv - last_net.bytes_recv) * 8 / elapsed_time / 1000 # в битах/с
        upload_load = (current_net.bytes_sent - last_net.bytes_sent) * 8 / elapsed_time / 1000  # в битах/с

        # download_load = (download_speed / max_bandwidth) * 100
        # upload_load = (upload_speed / max_bandwidth) * 100

        update_network_data({"download": round(download_load, 2), "upload": round(upload_load,2)})

