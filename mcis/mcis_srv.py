import secrets
import socket
import config
import sql_function
import func
import json
import queue

class mcis_srv:
    def __init__(self, data_queue):
        self.db = sql_function.sql_func(config.database_name)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((f'{config.server_host[0]}', config.server_host[1]))
        self.data_queue = data_queue  # Очередь для передачи данных в основной поток

    def start_mcis_srv(self):
        while True:
            message, client_address = self.server_socket.recvfrom(1024)
            print(message.decode())

            if message.decode() == "I Here!":
                if self.db.insert_host(client_address[0], 990, secrets.token_hex(16)):
                    print(self.db.show_all_hosts())
                    self.server_socket.sendto(b"OK", client_address)
                    func._elogs(f"Пользователь ip {client_address} зарегистрирован", ecode = 200)
                else:
                    self.server_socket.sendto(b"not Ok", client_address)
                    func._elogs(f"Пользователь ip {client_address} уже зарегистрирован", ecode = 200)

            elif self.db.get_api_by_ip(client_address[0]) == json.loads(message.decode())["api"]:
                print("Успешная регистрация")
                func._elogs(f"Авторизован ip {client_address}", ecode = 200)
                data = json.loads(message.decode())  
                print(data)
                
                # Добавляем данные в очередь
                self.data_queue.put(data)
                
                continue

            else:
                func._elogs(f"Не авторизован ip {client_address}", ecode = 200)
