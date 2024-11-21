from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/hello")
def hello_world():
    return "<p>Hello, saucisse!</p>"


app.run(host="0.0.0.0", port=8080, debug=True)