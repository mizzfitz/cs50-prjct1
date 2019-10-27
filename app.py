from flask import Flask, request, session, redirect, url_for
from flask_session import Session

from html_render import render
from databases import Books, Reviews, Users, Usr, User
from session_manager import log_rt, check_lang, resume_sess

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = Users()
books = Books()
reviews = Reviews()

@app.route("/", methods=["GET", "POST"])
@app.route("/<string:search_key>", methods=["GET", "POST"])
def index(search_key=""):
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        if search_key == "":
            search_key = request.form.get("search")
        return search_key
    return render(app.root_path, "index", session["usr"])

@app.route("/lang", methods=["GET", "POST"])
def get_lang():
    check_lang()
    if session["usr"].pref_lang != "":
        return resume_sess()
    if request.method == "POST":
        l = request.form.get("lang")
        if l == "fr" or l == "en":
            session["usr"].pref_lang = l
            return resume_sess()
        else:
            return redirect(url_for("get_lang"))
    else:
        return render(app.root_path,"lang", session["usr"])

@app.route("/login", methods=["GET", "POST"])
def login():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        uid = users.check_login(request.form.get("usr_name"), request.form.get("passwd"))
        if uid == 0:
            return render(app.root_path,"login", session["usr"], "err-login")
        session["usr"] = users.login(uid)
        return resume_sess()
    return render(app.root_path,"login", session["usr"])

@app.route("/create-account", methods=["GET", "POST"])
def sign_up():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        form = User(request.form.get("usr_name"), request.form.get("passwd1"), request.form.get("pref-lang"), request.form.get("lang"))
        test = users.check_new_usr(form, request.form.get("passwd2"))
        if test == "err-usr-name" or test == "err-no-lang" or test == "err-passwd":
            return render(app.root_path, "sign_up", session["usr"], test)
        elif test == "success":
            users.add_usr(form)
            session["usr"] = form
            return resume_sess()
        else:
            return render(app.root_path, "sign_up", session["usr"], "err-unknown")
    return render(app.root_path, "sign_up", session["usr"])

@app.route("/book", methods=["GET"])
def book():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    return "Book page"

@app.route("/logout")
def logout():
    session["usr"] = Usr(None, session["usr"].pref_lang, 0)
    return redirect(url_for("index"))
