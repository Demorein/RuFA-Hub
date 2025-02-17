import sys
import os
import threading
import queue
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_interface')))

from web_interface.app import app
from web_interface.data_handler import update_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mcis')))
from mcis.mcis_srv import mcis_srv

data_queue = queue.Queue()

server = mcis_srv(data_queue)
server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)

def process_data():
    while True:
        try:
            data = data_queue.get(timeout=1)
            print("Получены данные из MCIS:", data)

            update_data(data)

        except queue.Empty:
            continue

data_thread = threading.Thread(target=process_data, daemon=True)

def run_flask():
    app.run(host="192.168.203.57", port=5001, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)


    flask_thread.start()
    server_thread.start()
    data_thread.start()


    while True:
        time.sleep(1)