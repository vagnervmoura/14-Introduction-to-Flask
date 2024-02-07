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

app = Flask(__name__)
app.config["SECRET_KEY"] = "mySecretKey"

@app.route("/")
def index():
    return render_template("index.html", title="Vignoto - Accounting and Management System")


@app.route("/purchase/")
def purchase():
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