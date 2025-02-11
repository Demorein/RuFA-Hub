import sys
import os
import threading
import queue


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mcis')))

from mcis.mcis_srv import mcis_srv 


data_queue = queue.Queue()


server = mcis_srv(data_queue)
server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)
server_thread.start()


while True:
    try:
        data = data_queue.get(timeout=1)
        print("Получены данные из MCIS:", data)

    except queue.Empty:
        continue
