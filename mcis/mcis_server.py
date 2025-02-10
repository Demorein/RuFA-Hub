#MCIS Server

import socket
import config


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((f'{config.server_host[0]}', {config.server_host[1]}))

while True:
    message, client_address = server_socket.recvfrom(1024)
    print(message.decode())
    server_socket.sendto(b"OK", client_address)
