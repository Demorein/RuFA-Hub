import sys
import os
from queue import Queue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mcis.mcis_srv import mcis_srv
import socket
from config.cord import cords




class iot_man:

    def __init__(self):
        data_queue = Queue()
        self.mcis_server = mcis_srv(data_queue)
        self.host = ("192.168.203.121", 8888)

    def decode_message_for_iot_robots(self, data):
        print(data)
        # self.mcis_server.send_data(data, self.host)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = data["button"]

        data = cords[data].split(",")

        data = f"g:{data[0]}:{data[1]}:0:{data[2]}:0#"

        #g:x:y:v:z;0#

        print(data)


                    


        # Отправляем сообщение
        udp_socket.sendto(data.encode(), ("192.168.203.121", 8888))
        # Закрываем сокет
        udp_socket.close()


if __name__ == "__main__":
    a = iot_man()
    # a.decode_message_for_iot_robots("l:1:1:1:1#")
else: print("No __main__")
