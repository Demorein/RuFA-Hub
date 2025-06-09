import sys
import os
import threading
import queue
import time
import importlib
import core
import json

MODULES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
if MODULES_PATH not in sys.path:
    sys.path.append(MODULES_PATH)

# ----------------------Modules------------------------|
import modules.hardware_monitor                       #|
import modules.uptime                                 #|
from modules.hosts import hosts                       #|
from modules.network_monitor import get_network_load  #|
#------------------------------------------------------|

#-----------------------------Config---------------------------------|
from config.config import flask_host, server_host_udp, flask_debug  #|
#--------------------------------------------------------------------|

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_interface')))

from web_interface.app import app
from web_interface.data_handler import update_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mcis')))

from mcis.async_mcis_udp import mcis_srv
from mcis.async_mcis_tcp import mcis_srv_tcp

# from mcis.mcis_srv import mcis_srv
# from mcis.mcis_srv_tcp import mcis_srv_tcp

#Logger
Logger = core.Logger(__name__, "logs/main.log")

# Queue
data_queue = queue.Queue()
Logger.info("Initialization queue")

# TCP/UDP Servers queue
server = mcis_srv(data_queue)
server_tcp = mcis_srv_tcp(data_queue)
server_thread = threading.Thread(target=server.start_mcis_server, daemon=True)
server_thread_tcp = threading.Thread(target=server_tcp.start_mcis_server, daemon=True)


#Data Parser
import traceback

import traceback

def process_data():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))
    while True:
        try:
            raw_data = data_queue.get(timeout=1)
            Logger.info(f"Raw data from MCIS: {raw_data}")

            try:
                packets = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
                if isinstance(packets, dict):
                    packets = [packets]
            except json.JSONDecodeError as e:
                Logger.error(f"Failed to decode JSON from MCIS data: {e}")
                continue

            for i, packet in enumerate(packets):
                module_name = packet.get("module")
                if not module_name:
                    Logger.warning(f"Packet {i} is missing 'module' key: {packet}")
                    continue

                if f"{module_name}.py" not in core.Core_Module_Finder().module_list():
                    Logger.warning(f"Module '{module_name}' not found in list.")
                    continue

                try:
                    mod = importlib.import_module(module_name)
                except Exception as e:
                    err_msg = f"Failed to import module '{module_name}' for packet {i}: {e}"
                    Logger.error(err_msg)
                    Logger.error(traceback.format_exc())
                    continue  # Переходим к следующему пакету

                if hasattr(mod, "mainloop"):
                    try:
                        mod.mainloop(packet)
                    except Exception as e:
                        err_msg = f"Exception inside module '{module_name}' mainloop for packet {i}: {e}"
                        Logger.error(err_msg)
                        Logger.error(traceback.format_exc())
                else:
                    Logger.warning(f"Module '{module_name}' does not contain a mainloop() function.")

                update_data(packet)

        except queue.Empty:
            continue






data_thread = threading.Thread(target=process_data, daemon=True)
Logger.info("Initialization of basic flows")

def run_flask():
    app.run(host=f"{flask_host[0]}", port=flask_host[1], debug=flask_debug, use_reloader=False)

if __name__ == "__main__":

    Logger.info("Launch of basic flows")

    try:
        Logger.info("Initialization of basic modules")
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        hardware_pars = threading.Thread(target=modules.hardware_monitor.get_system_info, daemon=True)
        uptime_pars = threading.Thread(target=modules.uptime.uptime_parcer, daemon=True)
        network_data = threading.Thread(target=get_network_load, daemon=True)

        #Modules
        hosts(flask_host, server_host_udp)
        network_data.start()
        hardware_pars.start()
        uptime_pars.start()
        Logger.info("Launch of basic modules")

        #Main service
        flask_thread.start()
        server_thread.start()
        server_thread_tcp.start()

        data_thread.start()

        Logger.info("Launch of the main flows")


        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        os.system("export FLASK_ENV=development")

        print("\n\n\nThe server is stopped by the user")
        print(f"\nflask_host = {flask_host}\nMCIS_host = {server_host_udp}")
        Logger.info("The server is stopped by the user")
    except Exception as e:
        print(f"\n\n--- Error! ---\n\n{e}")
        print(f"\n\nflask_host = {flask_host}\nMCIS_host = {server_host_udp}")
        Logger.critical(e)





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

