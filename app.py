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
def index():
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    if not request.form.get("search"):
        return renderer.render("index", session["usr"])
    db = {"books": books.search(request.form.get("search"))}
    return renderer.render("search", session["usr"], db=db)

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
            return renderer.render("login", session["usr"], err="err-login")
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
            return renderer.render("sign_up", session["usr"], err=test)
        else:
            if users.add_usr(form):
                session["usr"] = form
                return resume_sess()
            else:
                return renderer.render("sign_up", session["usr"], err="err-unknown")
    return renderer.render("sign_up", session["usr"])

@app.route("/book/<string:isbn>", methods=["GET"])
def book(isbn):
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    db = {"book": books.get_by_isbn(isbn)}
    db["comments"] = reviews.get_by_book_id(db["book"]["book"].id)
    return renderer.render("book", session["usr"], db=db)

@app.route("/review/<string:isbn>", methods=["GET", "POST"])
def review(isbn):
    log_rt()
    if session["usr"].usr_name == None:
        return renderer.render("review_err", session["usr"])
    return "reviews here"

@app.route("/logout")
def logout():
    session["usr"] = Usr(None, session["usr"].pref_lang, 0)
    return redirect(url_for("index"))
