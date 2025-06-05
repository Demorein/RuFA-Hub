import asyncio
import sys
import os
import users
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config
from core import Logger

class mcis_srv_tcp:
    def __init__(self):
        self.users = users.users()
        self.Logger = Logger(__name__, "log/mcis_tcp.log")
        self.packets = {}  # { ip: [packet1, packet2, ...] }

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        ip = addr[0]
        self.Logger.info(f"New connection from {addr}")

        try:
            while True:
                data = await reader.readline()
                if not data:
                    self.Logger.info(f"Connection closed by {addr}")
                    break

                try:
                    packet_json = json.loads(data.decode().strip())
                except Exception as e:
                    self.Logger.warning(f"Failed to decode JSON from {addr}: {e}")
                    continue

                api_key = packet_json.get("api")
                if api_key and self.users.auth(addr, api_key):
                    if ip not in self.packets:
                        self.packets[ip] = []
                    self.packets[ip].append(packet_json)
                else:
                    self.Logger.info(f"Unauthorized access from {addr}")

        except Exception as e:
            self.Logger.error(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def process_packets(self):
        while True:
            await asyncio.sleep(2)
            for ip, packet_list in self.packets.items():
                combined = {}
                for i, pkt in enumerate(packet_list, 1):
                    combined[f"data{i}"] = pkt
                combined_json = json.dumps(combined, ensure_ascii=False)
                self.Logger.info(f"Combined packet from {ip}: {combined_json}")
                print(f"Combined packet from {ip}: {combined_json}")
            self.packets.clear()

    async def main(self):
        self.Logger.info("Starting MCIS TCP server")
        server = await asyncio.start_server(
            self.handle_client,
            config.server_host_tcp[0],
            config.server_host_tcp[1]
        )

        async with server:
            await asyncio.gather(
                server.serve_forever(),
                self.process_packets()
            )

    def start_mcis_server(self):
        try:
            asyncio.run(self.main())
        except Exception as e:
            self.Logger.error(f"Error in mcis_tcp: {e}")



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