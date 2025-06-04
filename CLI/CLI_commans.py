import os
import asyncio

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




