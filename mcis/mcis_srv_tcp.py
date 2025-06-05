import secrets
import socket
import json
import queue
import threading
import sql_function
import sys
import os

# Добавляем путь к config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config
import core

class mcis_srv_tcp:
    def __init__(self, data_queue):
        self.Logger = core.Logger(__name__, "logs/mcis_tcp.log")

        self.db = sql_function.sql_func(config.database_name)  # Класс работы с базой
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((config.server_host_tcp[0], config.server_host_tcp[1]))
        self.server_socket.listen(5)  # Максимум 5 ожидающих подключений
        self.data_queue = data_queue

    def handle_client(self, client_socket, client_address):

        buffer = b""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    self.Logger.info(f"Client {client_address} disconnected")
                    break
                buffer += data

                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    message = line.decode()

                    if message == "I Here!":
                        if self.db.insert_host(client_address[0], 990, secrets.token_hex(16)):
                            print(self.db.show_all_hosts())
                            client_socket.sendall(b"OK\n")
                            self.Logger.info(f"Client {client_address} registered")
                        else:
                            client_socket.sendall(b"not Ok\n")
                            self.Logger.info(f"User IP {client_address} is already registered")
                    else:
                        try:
                            data_json = json.loads(message)
                        except json.JSONDecodeError:
                            self.Logger.error(f"JSON Error from {client_address}")
                            client_socket.sendall(b"Invalid JSON\n")
                            continue

                        api_from_db = self.db.get_api_by_ip(client_address[0])
                        if api_from_db == data_json.get("api"):
                            self.Logger.info(f"Authorized IP {client_address}")
                            self.data_queue.put(data_json)
                            client_socket.sendall(b"Data received\n")
                        else:
                            self.Logger.info(f"Unauthorized ip {client_address}")
                            client_socket.sendall(b"Unauthorized\n")

        except Exception as e:
            self.Logger.exception(f"Client processing error with {client_address}: {e}")
        finally:
            client_socket.close()
            self.Logger.info(f"Connection with the client {client_address} closed")

    def start_mcis_srv(self):
        self.Logger.info(f"MCIS TCP has started ip {config.server_host_tcp[0]}:{config.server_host_tcp[1]}")

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True)
                thread.start()
            except Exception as e:
                self.Logger.error(f"Error in the main server cycle:{e}")
                


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