import sys
import os
import threading
import queue
import time

# Добавляем web_interface в sys.path, чтобы корректно импортировать файлы
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_interface')))

from web_interface.app import app  # <-- Импортируем объект Flask-приложения
from web_interface.data_handler import update_data  # Импортируем update_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mcis')))
from mcis.mcis_srv import mcis_srv

data_queue = queue.Queue()

# Запускаем сервер MCIS
server = mcis_srv(data_queue)
server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)

# Функция для обработки данных
def process_data():
    while True:
        try:
            data = data_queue.get(timeout=1)
            print("Получены данные из MCIS:", data)

            # Обновляем данные в web_interface/data_handler.py
            update_data(data)

        except queue.Empty:
            continue

# Запуск обработки данных в отдельном потоке
data_thread = threading.Thread(target=process_data, daemon=True)

# Функция для запуска Flask-сервера
def run_flask():
    app.run(host="192.168.203.57", port=5001, debug=False, use_reloader=False)  # Фикс: отключаем reloader

if __name__ == "__main__":
    # Запускаем Flask сервер в другом потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)

    # Стартуем потоки
    flask_thread.start()
    server_thread.start()
    data_thread.start()

    # Основной цикл, который не блокирует потоки
    while True:
        time.sleep(1)  # Даем возможность потокам работать
