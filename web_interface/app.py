from flask import Flask, render_template, jsonify, request, redirect, url_for
from web_interface.data_handler import get_latest_data, get_latest_hardware_data, get_latest_uptime_data, get_latest_host_data, get_latest_network_data
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.iot_module import iot_man

app = Flask(__name__)

@app.route("/")
def home_redirect():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/controllers")
def controllers():
    return render_template("controllers.html")

@app.route("/manipulator")
def manipulator():
    return render_template("manipulator.html")

#---------------------------------------------------------------
# URL REQUESTS

@app.route("/get_data")
def get_data():
    return jsonify({"data": get_latest_data()})

@app.route("/get_hardware_data")
def get_hardware_data():
    hd = get_latest_hardware_data()
    #return jsonify({"CPU": 20, "RAM": 50})
    return jsonify({"CPU": hd["CPU"], "RAM": hd["RAM"]})

@app.route("/get_uptime_data")
def get_uptime_data():
    uptime = get_latest_uptime_data()
    return jsonify({"h": uptime["h"], "m":uptime["m"]})

@app.route("/get_hosts_data")
def get_host_data():
    host_data = get_latest_host_data()
    return jsonify({"flhost": host_data["flhost"], "srvhost": host_data["srvhost"]})

@app.route("/get_network_data")
def get_network_data():
    network_data = get_latest_network_data()
    return jsonify({"download": network_data["download"], "upload": network_data["upload"]})

@app.route("/get_button", methods=["POST"])
def get_button():
    # try:
        # Получаем данные из тела запроса (предположим, что это JSON)
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")  # Логируем полученные данные для отладки
        obj = iot_man()
        obj.decode_message_for_iot_robots(data)


        # Проверяем, есть ли данные и ключ "button"
        if data and 'button' in data:
            button_name = data['button']
            app.logger.debug(f"Button clicked: {button_name}")  # Логируем, что кнопка была нажата

            # Возвращаем успешный ответ с данными кнопки
            return jsonify({"status": "success", "message": f"Button {button_name} clicked"}), 200
        else:
            # Если данных нет или они некорректные, возвращаем ошибку
            app.logger.error("Invalid data or missing 'button' key")  # Логируем ошибку
            return jsonify({"status": "error", "message": "Invalid data"}), 400
    # except Exception as e:
    #     # Логируем исключение, если оно произошло
    #     app.logger.error(f"Error occurred: {str(e)}")
    #     return jsonify({"status": "error", "message": str(e)}), 500
