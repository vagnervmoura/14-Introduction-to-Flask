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
warehouse = Manager(name="warehouse_file")

config_obj = Config()
config_obj.create_files()
manager = Manager(config_obj)

data = manager.load_data()

new_data = {}

app = Flask(__name__)
app.config["SECRET_KEY"] = "mySecretKey"
@app.route("/")
def index():
    data = manager.load_data()
    stock = data["v_warehouse"]
    balance = data["v_balance"]
    print(f"+++++++++++++++++++++++++++++ BALANCE: {balance}")
    # for stock in warehouse:
    #     print(stock)
    #     print(warehouse[stock]['v_quantity'])

    print(f">>>>>>>>> INDEX: {stock}")
    return render_template("index.html", title="Vignoto - Accounting and Management System", stock=stock, balance=balance)


@app.route("/purchase/", methods=["POST", "GET"])
def purchase():
    data = manager.load_data()
    balance = data["v_balance"]
    if request.method == "POST":
        form_values = request.form
        new_data = {
            "v_name": str(form_values["v_name"]),
            "v_quantity": int(form_values["v_quantity"]),
            "v_price": float(form_values["v_price"]),
        }
        manager.f_purchase(new_data)
        return redirect(url_for("index"))
    return render_template("purchase.html", title="PURCHASE", balance=balance)


@app.route("/sale/", methods=["POST", "GET"])
def sale():
    success = False
    data = manager.load_data()
    stock = data["v_warehouse"]
    if request.method == "POST":
        print(f">>>>>>>>>>>>>>>>>>>>>>>REQUEST: {request.form.get}")
        if request.form.get("s_name"):
            new_sale = {
                "s_name": request.form["s_name"],
                "s_quantity": request.form["s_quantity"]
            }
            if int(new_sale["s_quantity"]) > stock[new_sale["s_name"]]["v_quantity"]:
                print(f"Sorry, you do not have enough {new_sale['s_name']} to sell.\n")
                success = False
            else:
                success = manager.f_sale(new_sale)

            if not success:
                flash(f"Sorry no more '{new_sale['s_name']}' available!")
            else:
                flash(f"Successfully sold '{new_sale['s_quantity']}' items of '{new_sale['s_name']}'")

        return redirect(url_for("index"))


@app.route("/balance/", methods=["POST", "GET"])
def balance():
    data = manager.load_data()
    balance = data["v_balance"]
    if request.method == "POST":
        form_values = request.form
        # if request.form.get("1"):
        new_balance = {
            "v_value": float(form_values["v_value"]),
            "v_action": int(form_values["v_action"]),
        }
        print(f"++++++++++++++++++++++++++++++++++++++++++++++++ NEW BALANCE: {new_balance}")
        manager.f_balance(new_balance)
        return redirect(url_for("index"))
    return render_template("balance.html", title="BALANCE", balance=balance)


@app.route("/history/")
def history():
    data = manager.load_data()
    balance = data["v_balance"]
    return render_template("history.html", title="HISTORY", balance=balance)

#purchase()