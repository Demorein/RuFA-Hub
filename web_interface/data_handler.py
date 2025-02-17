import json

# Дефолтные данные (в виде словаря)
latest_data = {"data": "Ожидание данных..."}

def update_data(new_data):
    global latest_data
    if isinstance(new_data, dict) and "data" in new_data:
        latest_data = {"data": new_data["data"]}  # Записываем только ключ "data"
    else:
        latest_data = {"data": "Некорректные данные"}  # Обработка ошибки

def get_latest_data():
    print(json.dumps(latest_data["data"]))  # Выводим JSON-данные
    return latest_data["data"]  # Возвращаем словарь
