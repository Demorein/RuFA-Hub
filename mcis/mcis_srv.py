import secrets
import socket
import json
import queue
import func
import sql_function
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

class mcis_srv:
    def __init__(self, data_queue):
        self.db = sql_function.sql_func(config.database_name)  # Здесь используется sql_function
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((f'{config.server_host_udp[0]}', config.server_host_udp[1]))
        self.data_queue = data_queue  # Очередь для передачи данных в основной поток

    def start_mcis_srv(self):
        func._elogs(f"MCIS Сервер запущен на ip {config.server_host_udp[0]}", ecode = 200)
        while True:
            message, client_address = self.server_socket.recvfrom(1024)
            print(message.decode())
            func._elogs(f"Пакет данных от {client_address}", ecode = 200)

            if message.decode() == "I Here!": #Регистрация пользователей
                if self.db.insert_host(client_address[0], 990, secrets.token_hex(16)):
                    print(self.db.show_all_hosts())
                    self.server_socket.sendto(b"OK", client_address)
                    func._elogs(f"Пользователь ip {client_address} зарегистрирован", ecode = 200)
                else:
                    self.server_socket.sendto(b"not Ok", client_address)
                    func._elogs(f"Пользователь ip {client_address} уже зарегистрирован", ecode = 200)

            elif self.db.get_api_by_ip(client_address[0]) == json.loads(message.decode())["api"]: #Приём данных/Проверка токена
                print("Успешная авторизация")
                func._elogs(f"Авторизован ip {client_address}", ecode = 200)
                data = json.loads(message.decode())
                print(data)
                
                # Добавляем данные в очередь
                self.data_queue.put(data)
                
                continue

            else:
                func._elogs(f"Не авторизован ip {client_address}", ecode = 200)



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
