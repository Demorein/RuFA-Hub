import logging
import os

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
        self.module_dir = "modules"
        self.files = [f for f in os.listdir("modules/") if os.path.isfile(os.path.join("modules/", f))]

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
                with open(file_path, "r") as f:
                    parts = f.read().split("#$%^&*")[1]
                    return parts
            except Exception as e:
                return "Info Error"
  


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