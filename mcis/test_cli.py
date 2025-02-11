# MCIS client

import socket

a = {"data":"datata","api":"9d3af19f2554e7ccd2839d09ff82283b"}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(a.encode(), ('127.0.0.1', 12345))
print("I Here!")

response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()
