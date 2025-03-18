import json

# Дефолтные данные (в виде словаря)
harware_data = {"CPU": "Нет данных", "RAM": "Нет данных"}
latest_data = {"data": "Ожидание данных..."}

def update_data(new_data):
    global latest_data
    if isinstance(new_data, dict) and "data" in new_data:
        latest_data = {"data": new_data["data"]}  # Записываем только ключ "data"
    else:
        latest_data = {"data": "Некорректные данные"}  # Обработка ошибки

def update_hardware_data(new_data):
    global harware_data
    harware_data = {"CPU": new_data["CPU"], "RAM": new_data["RAM"]}

def get_latest_data():
    print(json.dumps(latest_data["data"]))  # Выводим JSON-данные
    return latest_data["data"]  # Возвращаем словарь

def get_latest_hardware_data():
    return harware_data
