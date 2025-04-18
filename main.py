import sys
import os
import threading
import queue
import time
from mcis.func import _elogs
# ----------------------Modules------------------------|
import modules.hardware_monitor                       #|
import modules.uptime                                 #|
from modules.hosts import hosts                       #|
from modules.network_monitor import get_network_load  #|
#------------------------------------------------------|

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
# server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)

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

    with open("modules/asd.txt", "w", encoding="utf-8") as file:
        print("Запись")
        file.write("200,0,90,0")
        print("Записано")

    # try:

        flask_thread = threading.Thread(target=run_flask, daemon=True)
        hardware_pars = threading.Thread(target=modules.hardware_monitor.get_system_info, daemon=True)
        uptime_pars = threading.Thread(target=modules.uptime.uptime_parcer, daemon=True)
        network_data = threading.Thread(target=get_network_load, daemon=True)


        #Modules
        hosts(flask_host, server_host)
        network_data.start()
        hardware_pars.start()
        uptime_pars.start()


        #Main service
        flask_thread.start()
        # server_thread.start()
        #data_thread.start()

        


        while True:
            time.sleep(1)
    # except KeyboardInterrupt:
    #     os.system("export FLASK_ENV=development")
    #     _elogs(f"Сервер неожиданно завершил работу", ecode = 500, v="error")
    #     print("\n\n\nСервер остановлен пользователем")
    #     print(f"\nflask_host = {flask_host}\nMCIS_host = {server_host}")

    # except Exception as e:
    #     print(f"\n\n--- Ошибка! ---\n{e}")
    #     print(f"\n\nflask_host = {flask_host}\nMCIS_host = {server_host}")