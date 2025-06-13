import importlib.util
import logging
import os
import yaml
import json
import queue
import threading

class Logger:
    def __init__(self, name: str, logfile: str = None):
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

            # Консоль
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # Файл (если указан)
            if logfile:
                os.makedirs(os.path.dirname(logfile), exist_ok=True)
                fh = logging.FileHandler(logfile, encoding="utf-8")
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)
    def exception(self, msg): self.logger.exception(msg)

class Core_Module_Finder:

    def __init__(self):
        self.module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
        self.files = [f for f in os.listdir(self.module_dir) if os.path.isdir(os.path.join(self.module_dir, f))]

    def module_list(self, function:str = "list"):
        if function == "list":
            return self.files
        else:
            return "\n".join(self.files)
    
    def module_info(self, module_name:str):
        file_path = os.path.join(self.module_dir, f"{module_name}.py")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Модуль {module_name} не найден")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                parts = f.read().split("#$%^&*")[1]
                return parts
        except Exception as e:
            return "Info Error"
        
def system_info():
    import platform
    return [f"{platform.system()} {platform.release()}", platform.node(), platform.version(), platform.machine(), platform.processor(), f"Python {platform.python_version()}"]

#FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME#
################ Добавить то, чтобы если очередь есть, то покет в очерель сувался#########################FIXME#
#FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME##########FIXME#

class process_data:
    def __init__(self, queue):
        self.data_queue = queue
        self.Logger = Logger(__name__, "core.log")
        self.queues = {}

    # Получает сырые данные
    def process_data(self):
        while True:
            try:

                raw_data = self.data_queue.get(timeout=1)
                self.Logger.info(f"Raw data from MCIS: {raw_data}")
                self.cut_data(raw_data)

            except Exception as e:
                pass

    # Запуск модуля (Тут происходит весь движ)
    def start_module(self, data:json):
        
        module_type = self.get_start_module_type(data)

        if module_type == "once":
            self.run_modules_once(data)
        elif module_type == "loop":
            id = self.get_module_ID(data)
            queue = self.create_queue(id)
            self.run_module_loop(data, queue)

    # Получение типа модуля (как его запускать)
    def get_start_module_type(self, data: json):
        module = data["module"]
        with open(f"modules/{module}/config.yml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file).get("launch_mode")

    # Резка пакета
    def cut_data(self, raw_data:list) -> json:
            for i in range(len(raw_data)):
                self.start_module(raw_data[i])

    # Создание новой очереди для модуля
    def create_queue(self, id: int) -> queue.Queue:
        if id in self.queues:
            return self.queues[id]
        self.queues[id] = queue.Queue()
        return self.queues[id]


    # Получить ID модуля
    def get_module_ID(self, data:json) -> int:
        module = data["module"]
        with open(f"module/{module}/config.yml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file).get("ID")
 

    def run_module_loop(self, data, queue):
        module_name = data.get("module")
        path = f"modules/{module_name}"

        if not os.path.isdir(path):
            return

        with open(f"{path}/config.yml", "r") as f:
            cfg = yaml.safe_load(f)

        if cfg.get("launch_mode") != "loop":
            return

        main_file = cfg.get("main_file")
        main_func_name = cfg.get("main_function")

        spec = importlib.util.spec_from_file_location(f"{module_name}_main", f"{path}/{main_file}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, main_func_name):
            func = getattr(mod, main_func_name)
            thread = threading.Thread(target=func, args=([data, queue],))
            thread.daemon = True  # чтобы поток не мешал закрытию программы
            thread.start()


    # Запуск модуля один раз
    def run_module_once(self, data):
        module_name = data.get("module")
        path = f"modules/{module_name}"

        if not os.path.isdir(path):
            return

        with open(f"{path}/config.yml", "r") as f:
            cfg = yaml.safe_load(f)

        if cfg.get("launch_mode") != "once":
            return

        main_file = cfg.get("main_file")
        main_func_name = cfg.get("main_function")

        spec = importlib.util.spec_from_file_location(f"{module_name}_main", f"{path}/{main_file}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, main_func_name):
            getattr(mod, main_func_name)(data)


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