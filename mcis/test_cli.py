# MCIS client

import socket
import json

a = {"data":"123","api":"81065eb0a9542865c47320e6de3d6e3a"}
b = "L:123,123,123,123,123,123"
c = "M:123,123,123,123,123,123"
d = "T:123,123,123,123,123,123"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(json.dumps(a).encode(), ('192.168.203.22', 8888))
client_socket.sendto(json.dumps(b).encode(), ('192.168.203.22', 8888))
client_socket.sendto(json.dumps(c).encode(), ('192.168.203.22', 8888))
client_socket.sendto(json.dumps(d).encode(), ('192.168.203.22', 8888))
#client_socket.sendto("I Here!".encode(), ('127.0.0.1', 12345))
print("I Here!")

response = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
