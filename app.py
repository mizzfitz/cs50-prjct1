from flask import Flask
from html_render import render
from databases import *

app = Flask(__name__)

@app.route("/")
def index():
    return render(0)

