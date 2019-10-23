from flask import Flask
from html_render import render

app = Flask(__name__)

@app.route("/")
def index():
    usr = {}
    return render(app.root_path,"index", usr)

