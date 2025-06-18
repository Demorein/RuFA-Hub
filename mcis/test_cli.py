# MCIS client

import socket
import json

a = {
     "module":"example_module_loop",
     "api":"46fb95a876e6a83eadfcf2d8820f1421",
     "data":"Test Logs"
     }

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(json.dumps(a).encode(), ('192.168.203.100', 1201))
#client_socket.sendto("I Here!".encode(), ('127.0.0.1', 12345))
print("I Here!")

response, _ = client_socket.recvfrom(1024)
print(response.decode())
client_socket.close()




# RuFA-Hub
# Copyright (C) 2025 Gromov Evgeniy Vyacheslavovich

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 2 for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
