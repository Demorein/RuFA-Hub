from flask import Flask, render_template, jsonify
from web_interface.data_handler import get_latest_data  # Правильный импорт из той же папки

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    return jsonify({"data": get_latest_data()})  # Отдаём последние данные
