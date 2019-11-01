import os, sys

from flask import Flask, request, session, redirect, url_for
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from html_render import Renderer
from databases import Books, Reviews, Users, Usr, User
from session_manager import log_rt, check_lang, resume_sess

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if not os.getenv("DATABASE_URL"):
    print("Environment variable DATABASE_URL must be defined")
    sys.exit(1)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

users = Users(db)
books = Books(db)
reviews = Reviews(db)

renderer = Renderer(app.root_path)

@app.route("/", methods=["GET", "POST"])
@app.route("/<string:search_key>", methods=["GET", "POST"])
def index(search_key=""):
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        return ""
    return renderer.render("index", session["usr"])

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
        return renderer.render("lang", session["usr"])

@app.route("/login", methods=["GET", "POST"])
def login():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        #return str(users.check_login(request.form.get("usr_name"), request.form.get("passwd")))
        if not users.check_login(request.form.get("usr_name"), request.form.get("passwd")):
            return renderer.render("login", session["usr"], "err-login")
        session["usr"] = users.login(request.form.get("usr_name"))
        return resume_sess()
    return renderer.render("login", session["usr"])

@app.route("/create-account", methods=["GET", "POST"])
def sign_up():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if request.method == "POST":
        form = User(request.form.get("usr_name"), request.form.get("passwd1"), request.form.get("pref-lang"), request.form.get("lang"))
        test = users.check_new_usr(form, request.form.get("passwd2"))
        if test == "err-usr-name" or test == "err-no-lang" or test == "err-passwd":
            return renderer.render("sign_up", session["usr"], test)
        else:
            if users.add_usr(form):
                session["usr"] = form
                return resume_sess()
            else:
                return renderer.render("sign_up", session["usr"], "err-unknown")
    return renderer.render("sign_up", session["usr"])

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
