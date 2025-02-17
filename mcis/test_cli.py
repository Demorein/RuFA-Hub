# MCIS client

import socket
import json

a = {"data":"datata","api":"ed5b041f2efdc50925e062f05565104e"}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(json.dumps(a).encode(), ('127.0.0.1', 12345))
#client_socket.sendto("I Here!".encode(), ('127.0.0.1', 12345))
print("I Here!")

response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
