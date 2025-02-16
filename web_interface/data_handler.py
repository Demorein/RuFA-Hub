# data_handler.py

latest_data = "Ожидание данных..."

def update_data(new_data):
    global latest_data
    latest_data = new_data  # Обновляем данные

def get_latest_data():
    return latest_data
