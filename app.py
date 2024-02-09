# flask run --debug
"""
{% extends "base.html" %}

{% block content %}

{% endblock %}
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from manager import Manager
from config import Config

db = Manager

config_obj = Config()
config_obj.create_files()
manager = Manager(config_obj)

data = manager.load_data()
new_data = {}

app = Flask(__name__)
app.config["SECRET_KEY"] = "mySecretKey"
@app.route("/")
def index():
    print(f">>>>>>>>> INDEX: {data}")
    return render_template("index.html", title="Vignoto - Accounting and Management System")


@app.route("/purchase/", methods=["POST", "GET"])
def purchase():
    if request.method == "POST":
        form_values = request.form
        new_data = {
            "v_name": str(form_values["v_name"]),
            "v_quantity": int(form_values["v_quantity"]),
            "v_price": float(form_values["v_price"]),
        }
        v_name = new_data["v_name"]
        v_quantity = new_data["v_quantity"]
        v_price = new_data["v_price"]
        total_price = v_price
        manager.f_purchase(new_data)
    return render_template("purchase.html", title="PURCHASE")


@app.route("/sale/")
def sale():
    return render_template("sale.html", title="SALE")


@app.route("/balance/")
def balance():
    return render_template("balance.html", title="BALANCE")


@app.route("/history/")
def history():
    return render_template("history.html", title="HISTORY")

#purchase()