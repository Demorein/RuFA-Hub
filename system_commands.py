import core

class SystemCommands:

    def __init__(self):
        pass

    class _logger:
        def __init__(self, name, logfile):

            """
            The function of the logistics class retains all the logs in the Logs/ accepts arguments:

            NAME - the name of the logical file

            Logfile - the name of the file in which the logs will be saved
            """

            self.logger = core.Logger(name, f"logs/{logfile}")

        def debug(self, msg): self.logger.debug(msg=msg)
        def info(self, msg): self.logger.info(msg=msg)
        def warning(self, msg): self.logger.warning(msg=msg)
        def error(self, msg): self.logger.error(msg=msg)
        def critical(self, msg): self.logger.critical(msg=msg)
        def exception(self, msg): self.logger.exception(msg=msg)


    class system_data:
        def __init__(self):
            pass

        def get_cpu(argument:str = None) -> tuple:

            """
            The function returns the workload of CPU / RAM, the arguments of the function

            h - returns the value of CPU / RAM for reading a person

            hb - Returns CPU / RAM to read by a person in bytes

            b - returns the motorcade where 0 cpu

            by default, returns in bytes a motorcade
            """


            from psutil import cpu_percent, virtual_memory

            cpu_usage = cpu_percent(interval=1)

            if argument == "h":
                ram_usage = virtual_memory().used / 1073741824
                return(f"CPU {cpu_usage}%", f"RAM {round(ram_usage, 2)} Gb")
            elif argument == "hb":
                ram_usage = virtual_memory().used
                return(f"CPU {cpu_usage}%", f"RAM {ram_usage}")
            elif argument == "b":
                ram_usage = virtual_memory().used
                return(cpu_usage, ram_usage)
            else:
                ram_usage = virtual_memory().used / 1073741824
                return(cpu_usage, ram_usage)
            

        def network() -> tuple:

            """
            The function returns tuple where 0 loading, 1 uploading
            """

            from psutil import net_io_counters
            from time import sleep, time

            max_bandwidth= 1000 * 1024 * 1024

            last_net = net_io_counters()
            last_time = time()

            current_net = net_io_counters()
            current_time = time()

            elapsed_time = current_time - last_time

            download_speed = (current_net.bytes_recv - last_net.bytes_recv) * 8 / elapsed_time  # в битах/с
            upload_speed = (current_net.bytes_sent - last_net.bytes_sent) * 8 / elapsed_time  # в битах/с

            download_load = (download_speed / max_bandwidth) * 100
            upload_load = (upload_speed / max_bandwidth) * 100

            return(round(download_load, 2), round(upload_load, 2))

        
        class MCIS:
            def __init__(self, host:tuple):
                self.host = host

            def mcis_udp(self, data):
                from mcis.async_mcis_udp import mcis_srv
                srv = mcis_srv()
                srv.send_data(data=data, host=self.host)




if __name__ == "__main__":
    host:tuple = ("192.168.203.39", 8888)
    a = SystemCommands.system_data.MCIS(host=host)
    
    a.mcis_udp("asd")



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