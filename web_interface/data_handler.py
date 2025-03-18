import json

#######--------------VARIABLES
harware_data = {"CPU": "Нет данных", "RAM": "Нет данных"}
uptime_data = {"h": "Нет данных", "m": "Нет данных"}
latest_data = {"data": "Ожидание данных..."}
hosts = {"flhost": "Нет данных", "srvhost": "Нет данных"}
network_data = {"download": "Нет данных", "upload": "Нет данных"}

#######--------------UPDATE

def update_data(new_data):
    global latest_data
    if isinstance(new_data, dict) and "data" in new_data:
        latest_data = {"data": new_data["data"]}  # Записываем только ключ "data"
    else:
        latest_data = {"data": "Некорректные данные"}  # Обработка ошибки


def update_hardware_data(new_data):
    global harware_data
    harware_data = {"CPU": new_data["CPU"], "RAM": new_data["RAM"]}


def update_uptime_data(new_data):
    global update_data
    update_data = {"h":new_data["h"], "m":new_data["m"]}


def update_host_data(new_data):
    global hosts
    flhost = new_data[0]
    srvhost = new_data[1]
    hosts = {"flhost": flhost, "srvhost": srvhost}


def update_network_data(new_data):
    global network_data
    network_data = {"download": new_data["download"], "upload": new_data["upload"]}


#######--------------GET

def get_latest_data():
    print(json.dumps(latest_data["data"]))  # Выводим JSON-данные
    return latest_data["data"]  # Возвращаем словарь


def get_latest_hardware_data():
    return harware_data


def get_latest_uptime_data():
    return update_data


def get_latest_host_data():
    return hosts


def get_latest_network_data():
    return network_data
