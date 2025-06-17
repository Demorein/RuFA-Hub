import importlib.util
import logging
import os
import yaml
import json
import queue
import threading
import inspect

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

class setup_module():
    def __init__(self):
        self.module_names = self.collect_module_configs()
        self.Logger = Logger(__name__, "logs/core.log")

    def collect_module_configs(self, path="./modules"):
        result = []
        for name in os.listdir(path):
            cfg = f"{path}/{name}/config.yml"
            if os.path.isdir(f"{path}/{name}") and os.path.isfile(cfg):
                with open(cfg) as f:
                    data = yaml.safe_load(f)
                    result.append({
                        "module_name": name,
                        "launch_mode": data.get("launch_mode"),
                        "id": data.get("ID")
                    })
        return result

    def setup(self):
        modules = self.collect_module_configs()
        loop_queues = []

        for mod in modules:
            if mod["launch_mode"] == "loop":
                mod_name = mod["module_name"]
                mod_id = mod["id"]
                mod_path = f"./modules/{mod_name}/main.py"

                try:
                    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
                    mod_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod_module)
                except Exception as e:
                    Logger.error(f"Ошибка загрузки модуля '{mod_name}': {e}")
                    continue

                # Проверяем функцию mainloop
                mainloop = getattr(mod_module, "mainloop", None)
                if not callable(mainloop):
                    Logger.error(f"В модуле '{mod_name}' отсутствует функция mainloop()")
                    continue

                # Проверяем количество аргументов у mainloop (должен быть 1)
                sig = inspect.signature(mainloop)
                params = sig.parameters
                if len(params) != 1:
                    Logger.error(f"Функция mainloop в модуле '{mod_name}' должна принимать ровно один аргумент (queue)")
                    continue

                # Запускаем поток с очередью
                q = queue.Queue()
                t = threading.Thread(target=mainloop, args=(q,), daemon=True)
                t.start()

                loop_queues.append({
                    "queue": q,
                    "id": mod_id
                })

        return loop_queues


class process_data:
    def __init__(self, modules_queue, modules_json_param, my_queue):
        self.modules_queue = modules_queue              # Очереди для loop-модулей
        self.modules_json_param = modules_json_param    # Данные о модулях
        self.my_queue = my_queue                        # Очередь входящих пакетов
        self.Logger = Logger(__name__, "core.log")

    def procces_data(self):
        while True:
            data_batch = self.my_queue.get()  # Ожидаем пакет
            data_batch = json.loads(data_batch)
            self.Logger.info(data_batch)
            for packet in data_batch:
                module_name = packet.get("module")
                module_info = self.get_id_modules(module_name)
                if not module_info:
                    continue

                mode = module_info["launch_mode"]
                if mode == "loop":
                    self.send_data_to_module_queue(packet, module_info["id"])
                elif mode == "once":
                    self.send_data_to_module_once(packet, module_info["module_name"])

    def send_data_to_module_queue(self, packet, target_id):
        for entry in self.modules_queue:
            if entry["id"] == target_id:
                entry["queue"].put(packet)
                break

    def send_data_to_module_once(self, packet, module_name):
        def runner():
            spec = importlib.util.spec_from_file_location(module_name, f"./modules/{module_name}/main.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.mainloop(packet)  # Без проверок, предполагаем что всё есть и правильно

        threading.Thread(target=runner, daemon=True).start()

    def get_id_modules(self, name):
        for module in self.modules_json_param:
            if module["module_name"] == name:
                return module
        return None


if __name__ == "__main__":
    from time import sleep
    import threading

    a = setup_module()
    b = a.collect_module_configs()
    print(b)
    queues = a.setup()
    print(queues)

    my_q = queue.Queue()

    pp = process_data(modules_queue = queues, modules_json_param = b, my_queue=my_q)

    th = threading.Thread(target=pp.procces_data, daemon=True)
    th.start()

    sleep(2)

    my_q.put([{"data": "AHAHAHAHAHA", "module": "example_module2", "api": "f7643450b89d5ef7867b1a92144cab58", "ip": "192.168.203.100"}])


    while True:
        sleep(1)
        continue


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