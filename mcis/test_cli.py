# MCIS client

import socket
import json

a = {"data":"datata","api":"20defd967db78f503464f5e8bc5ebb61"}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#client_socket.sendto(json.dumps(a).encode(), ('127.0.0.1', 12345))
client_socket.sendto("I Here!".encode(), ('127.0.0.1', 12345))
print("I Here!")

response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
