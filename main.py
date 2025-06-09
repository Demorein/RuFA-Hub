import sys
import os
import threading
import queue
import time
import importlib
import core

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
from mcis.mcis_srv import mcis_srv
from mcis.mcis_srv_tcp import mcis_srv_tcp

#Logger
Logger = core.Logger(__name__, "logs/main.log")

# Queue
data_queue = queue.Queue()
MSTB_queue = queue.Queue()
Logger.info("Initialization queue")

# TCP/UDP Servers queue
server = mcis_srv(data_queue)
server_tcp = mcis_srv_tcp(data_queue)
server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)
server_thread_tcp = threading.Thread(target=server_tcp.start_mcis_srv, daemon=True)


#Data Parser
def process_data():
    while True:
        try:
            data = data_queue.get(timeout=1)
            Logger.info(f"Data from MCIS: {data}")
            
            try:
                module_name = data["module"]

                # Check if the module exists in the list
                if f"{module_name}.py" not in core.Core_Module_Finder().module_list():
                    Logger.warning(f"Module '{module_name}' not found in list.")
                    continue

                # Dynamically import the module
                mod = importlib.import_module(f"module.{module_name}")

                # Check if the module has a mainloop() function
                if hasattr(mod, "mainloop"):
                    mod.mainloop(data)
                else:
                    Logger.warning(f"Module '{module_name}' does not contain a mainloop() function.")

            except Exception as e:
                Logger.error(f"Error in module '{module_name}': {e}")

            update_data(data)

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

