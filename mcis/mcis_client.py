# MCIS client

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("Привет".encode(), ('127.0.0.1', 12345))

response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
