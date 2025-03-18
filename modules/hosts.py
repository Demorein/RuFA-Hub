import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_interface.data_handler import update_host_data

def hosts(flhost, mcishost):
    update_host_data([flhost,mcishost])

    