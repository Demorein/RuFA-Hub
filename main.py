import sys
import os
import threading
import queue
import time
import modules.hardware_monitor
from config.config import flask_host, server_host, flask_debug
import psutil
import mcis.func

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
    app.run(host=f"{flask_host[0]}", port=flask_host[1], debug=flask_debug, use_reloader=False)

if __name__ == "__main__":
    try:

        flask_thread = threading.Thread(target=run_flask, daemon=True)
        hardware_pars = threading.Thread(target=modules.hardware_monitor.get_system_info, daemon=True)


        flask_thread.start()
        server_thread.start()
        data_thread.start()
        hardware_pars.start()


        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        os.system("export FLASK_ENV=development")
        func._elogs(f"Сервер неожиданно завершил работу", ecode = 500, v="error")
        print("\n\n\nСервер остановлен пользователем")
        print(f"\nflask_host = {flask_host}\nMCIS_host = {server_host}")

    except Exception as e:
        print(f"\n\n--- Ошибка! ---\n{e}")
        print(f"\n\nflask_host = {flask_host}\nMCIS_host = {server_host}")