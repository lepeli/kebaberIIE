from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"
