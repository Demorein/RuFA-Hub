import asyncio
import sys
import os

import config.config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

class mcis_srv:
    def __init__(self):
        self.host = config.server_host_udp
        self.db_name = config.database_name


    async def data_handler(self):
        pass

    async def create_udp_server(self):