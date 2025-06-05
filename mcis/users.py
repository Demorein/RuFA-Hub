import sys
import os
import secrets
import sql_function
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config
import core

class users:
    def __init__(self):
        self.db = config.database_name
        self.Logger = core.Logger(__name__, "logs/users.log")

    async def register(self, host):
        try:
            await self.db.insert_host(host[0], 990, secrets.token_hex(16))
            self.Logger.info(f"Successful registration;ip {host[0]}:OK")
            return "Successful registration:OK"
        except Exception as e:
            self.Logger.error(f"Registration error:ip {host[0]}:{e}")
            return f"Registration error:{e}"
        
    async def auth(self, host, api:str):
        try:
            if await self.db.get_api_by_ip(host[0]) == api:
                self.Logger.info(f"Successful authorization;ip {host[0]}:OK")
                return "Authorized"
            else:
                self.Logger.info(f"Unauthorized;ip {host[0]}:NONE")
                return "Unauthorized"
        except Exception as e:
            self.Logger.error(f"Authorization error:{e}")
            return "Authorization error"