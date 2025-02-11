import sys
import os
import threading
import queue

# Добавляем путь к mcis перед импортом!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mcis')))

from mcis.mcis_srv import mcis_srv  # Теперь импорт работает корректно

# Создаём очередь
data_queue = queue.Queue()

# Запускаем сервер в отдельном потоке
server = mcis_srv(data_queue)
server_thread = threading.Thread(target=server.start_mcis_srv, daemon=True)
server_thread.start()

# Основной поток: обработка данных из очереди
while True:
    try:
        data = data_queue.get(timeout=1)  # Получаем данные с таймаутом в 1 сек.
        print("Получены данные из MCIS:", data)
        # Здесь можно обработать данные, например, передать их в другую часть программы
    except queue.Empty:
        continue  # Если очередь пуста, продолжаем цикл
