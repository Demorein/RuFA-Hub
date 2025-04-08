from flask import Flask, render_template, jsonify, redirect, url_for
from web_interface.data_handler import get_latest_data, get_latest_hardware_data, get_latest_uptime_data, get_latest_host_data, get_latest_network_data

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
