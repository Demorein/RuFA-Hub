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
        self.server_socket.bind((f'{config.server_host[0]}', config.server_host[1]))
        self.data_queue = data_queue  # Очередь для передачи данных в основной поток

    def start_mcis_srv(self):
        func._elogs(f"MCIS Сервер запущен на ip {config.server_host[0]}", ecode = 200)
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
                print("Успешная регистрация")
                func._elogs(f"Авторизован ip {client_address}", ecode = 200)
                data = json.loads(message.decode())
                print(data)
                
                # Добавляем данные в очередь
                self.data_queue.put(data)
                
                continue

            else:
                func._elogs(f"Не авторизован ip {client_address}", ecode = 200)

