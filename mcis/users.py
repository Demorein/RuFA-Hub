import sys
import os
import secrets
import sql_function
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config
from core import Logger
import sql_function

class users:
    def __init__(self):
        self.db = sql_function.sql_func(config.database_name)
        self.Logger = Logger(__name__, "logs/users.log")

    def register(self, host):
        try:
            self.db.insert_host(host[0], 990, secrets.token_hex(16))
            self.Logger.info(f"Successful registration;ip {host[0]}:OK")
            return "Successful registration:OK", True
        except Exception as e:
            self.Logger.error(f"Registration error:ip {host[0]}:{e}")
            return f"Registration error:{e}", False
        
    def auth(self, host, api:str):
        try:
            if self.db.get_api_by_ip(host[0]) == api:
                self.Logger.info(f"Successful authorization;ip {host[0]}:OK")
                return "Authorized", True
            else:
                self.Logger.info(f"Unauthorized;ip {host[0]}:NONE")
                return "Unauthorized", False
        except Exception as e:
            self.Logger.error(f"Authorization error:{e}")
<<<<<<< HEAD
            return "Authorization error", False
        

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
=======
            return "Authorization error", False
>>>>>>> 482f874172339af4ef74f0e75345faff592d0f41
