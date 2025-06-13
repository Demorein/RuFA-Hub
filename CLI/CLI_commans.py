import os

#CLI

def list_files(directory):

    try:
        entries = os.listdir(directory)
        files = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
        return files, len(files)
    except FileNotFoundError:
        print(f"Директория '{directory}' не найдена.")
        return [], 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return [], 0


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

