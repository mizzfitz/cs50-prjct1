from flask import Flask, request, session, redirect, url_for
from flask_session import Session

from html_render import render
from databases import Books, Reviews, Users, Usr

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def check_lang():
    if session.get("usr") is None:
        session["usr"] = Usr(None)
        return True
    elif session["usr"].pref_lang == "":
        return True
    else:
        return False

@app.route("/<string:search_key>", methods=["GET", "POST"])
def index(search_key=""):
    if check_lang():
        return redirect(url_for("get_lang"))
    return "BiLingue"

@app.route("/lang", methods=["GET", "POST"])
def get_lang():
    if request.method == "POST":
        return "Great search"
    else:
        return render(app.root_path,"lang", session["usr"])

@app.route("/login", methods=["GET"])
def login():
    check_lang()
    return render(app.root_path,"login", session["usr"])

@app.route("/create-account", methods=["GET"])
def sign_up():
    check_lang()
    return "Create Account screen"

@app.route("/book", methods=["GET"])
def book():
    return "Book page"
