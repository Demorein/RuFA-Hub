import asyncio
import sys
import os
import socket
from mcis import users
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config
from core import Logger

#MCIS UDP
class mcis_srv:
    def __init__(self, data_queue):
        self.users = users.users()
        self.data_queue = data_queue
        self.Logger = Logger(__name__, "logs/mcis_udp.log")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((config.server_host_udp[0], config.server_host_udp[1]))
        self.packets = {}

    async def receive_packets(self):
        loop = asyncio.get_running_loop()
        while True:
            data, addr = await loop.run_in_executor(None, self.server_socket.recvfrom, 1024)
            packet_json = json.loads(data.decode())
            api_key = packet_json.get("api")
            if api_key and self.users.auth(addr, api_key):
                ip = addr[0]
                if ip not in self.packets:
                    self.packets[ip] = []
                self.packets[ip].append(packet_json)
            else:
                self.Logger.info(f"Unauthorized access from {addr}")

    async def send_data(self, data, host:tuple):
        await self.server_socket.sendto(data.encode(), host)

    async def process_packets(self):
        while True:
            await asyncio.sleep(2)
            combined_all = []

            for ip, packet_list in self.packets.items():
                for pkt in packet_list:
                    pkt_with_ip = {
                        "data": pkt.get("data"),
                        "module": pkt.get("module"),
                        "api": pkt.get("api"),
                        "ip": ip
                    }
                    combined_all.append(pkt_with_ip)

            if combined_all:
                combined_json = json.dumps(combined_all, ensure_ascii=False)
                self.Logger.info(f"Combined all packets: {combined_json}")
                self.data_queue.put(combined_json)

            self.packets.clear()


    async def main(self):
        self.Logger.info("Starting MCIS UDP server")
        await asyncio.gather(
            self.receive_packets(),
            self.process_packets()
        )

    def start_mcis_server(self):
        try:
            asyncio.run(self.main())
        except Exception as e:
            self.Logger.error(f"Error in mcis_udp: {e}")


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