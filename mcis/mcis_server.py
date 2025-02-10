#MCIS Server

import socket
import config
import sql_function

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((f'{config.server_host[0]}', config.server_host[1]))

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(message.decode())
    if sql_function.sql_func(config.database_name).insert_host(client_address[0], 990):
        server_socket.sendto(b"OK", client_address)
    else:
        server_socket.sendto(b"not Ok", client_address)
