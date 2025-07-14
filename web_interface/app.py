from flask import Flask, render_template, jsonify, redirect, url_for
import os
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

@app.route('/images')
def list_images():
    files = os.listdir('web_interface/static/images')
    image_files = [f'/static/images/{f}' for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(sorted(image_files))




# RuFA-Hub
# Copyright (C) 2025 Gromov Evgeniy Vyacheslavovich

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 2 for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
