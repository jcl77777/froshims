from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/froshims/register", method=["POST"])
def register():
    return render_template("success.html")