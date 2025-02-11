#MCIS Server

import socket
import config
import sql_function
import func

db = sql_function.sql_func(config.database_name)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((f'{config.server_host[0]}', config.server_host[1]))

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(message.decode())

    if message.decode() == "I Here!": 
        if db.insert_host(client_address[0], 990):
            print(db.show_all_hosts())
            server_socket.sendto(b"OK", client_address)
            func._elogs(f"Пользователь ip {client_address} зарегистрирован", ecode = 200)
        else:
            server_socket.sendto(b"not Ok", client_address)
            func._elogs(f"Пользователь ip {client_address} уже зарегистрирован", ecode = 200)
            db.delete_all_hosts()
    else:
        print("NoNoNo")
        func._elogs(f"Не зарегестрированный пользователь ip {client_address}", ecode = 200)
