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

@app.route("/")
@app.route("/<string:search_key>", methods=["GET", "POST"])
def index(search_key=""):
    if check_lang():
        return redirect(url_for("get_lang"))
    return "BiLingue"

@app.route("/lang", methods=["GET", "POST"])
def get_lang():
    check_lang()
    if request.method == "POST":
        return "Post"
    else:
        return render(app.root_path,"lang", session["usr"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        uid = check_login(request.form.get("usr_name"), request.form.get("passwd"))
        if uid == 0:
            return render(app.root_path,"login", session["usr"], "no-login")
    return render(app.root_path,"login", session["usr"])

@app.route("/create-account", methods=["GET", "POST"])
def sign_up():
    if check_lang():
        return redirect(url_for("get_lang"))
    return "Create Account screen"

@app.route("/book", methods=["GET"])
def book():
    if check_lang():
        return redirect(url_for("get_lang"))
    return "Book page"
