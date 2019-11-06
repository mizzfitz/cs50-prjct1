import os, sys

from flask import Flask, request, session, redirect, url_for, jsonify
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

""" Local imports from this package.  General architecture is:
    html_render.py contains class Renderer with functions to render html dynamicaly
    databases.py contains classes for managing user info (Usr, User) and all database interactions are through Books and Users
    (Books manages books and reviews databases and Users manages user database)
    session_manager has a handful of functions for session overhead """
from html_render import Renderer
from databases import Books, Users, Usr, User
from session_manager import log_rt, check_lang, resume_sess, goodreads_rev

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

# replace app.root_path with the path to your copy/ directory
renderer = Renderer(app.root_path)

@app.route("/", methods=["GET", "POST"])
def index():
    """ This function provides to home page for the site as well as rendering search results to
    user submitted searches """

    # overhead to check that we are serving the site in the users prefered language
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))

    # return home page if there was no search entry
    if not request.form.get("search"):
        return renderer.render("index", session["usr"])

    # compile and return a list of search results
    db = {"books": books.search(request.form.get("search"))}
    return renderer.render("search", session["usr"], db=db)

@app.route("/lang", methods=["GET", "POST"])
def get_lang():
    """ this function allows the user to input there prefered language and should be the first thing a new user encounters """
    check_lang()

    # if the user has somehow gotten to this route after choosing a prefered language we send them back to the main site
    if session["usr"].pref_lang != "":
        return resume_sess()

    # do the work of selecting user language and sending them to the main site
    if request.method == "POST":
        l = request.form.get("lang")
        if l == "fr" or l == "en":
            session["usr"].pref_lang = l
            return resume_sess()
        else:
            return redirect(url_for("get_lang"))

    # display language selection form if the user hasn't entered it
    return renderer.render("lang", session["usr"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """ the main login function. Pretty self-explanatory. """
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))

    if request.method == "POST":
        # check submited info and return to the form with an error message if it is incorrect, else redirect to the main website
        if not users.check_login(request.form.get("usr_name"), request.form.get("passwd")):
            return renderer.render("login", session["usr"], err="err-login")
        session["usr"] = users.login(request.form.get("usr_name"))
        return resume_sess()

    return renderer.render("login", session["usr"])

@app.route("/create-account", methods=["GET", "POST"])
def sign_up():
    """ function for a user to create an account """
    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))

    if request.method == "POST":
        # get the form info formated into a User object
        form = User(request.form.get("usr_name"), request.form.get("passwd1"), request.form.get("pref-lang"), request.form.get("lang"))

        # check_new_usr returns a string providing an error message key or a specific success string
        test = users.check_new_usr(form, request.form.get("passwd2"))
        # evaluate the response, sending an error message if we are given one
        if test == "err-usr-name" or test == "err-no-lang" or test == "err-passwd":
            return renderer.render("sign_up", session["usr"], err=test)
        else:
            # attempt to add the user to the database.  This function will return false if adding the user fails (should never occur but is included for managing potential race conditions)
            if users.add_usr(form):
                session["usr"] = form
                return resume_sess()
            # return an unknown error if for some reason adding the user to the database failed
            else:
                return renderer.render("sign_up", session["usr"], err="err-unknown")

    return renderer.render("sign_up", session["usr"])

@app.route("/book/<string:isbn>", methods=["GET"])
def book(isbn):
    """ function to display a books info and review based on a given isbn.  Linked to from search results
    Can redirect user to submit review function """

    log_rt()
    if check_lang():
        return redirect(url_for("get_lang"))
    db = {"book": books.get_by_isbn(isbn)}
    db["goodreads"] = goodreads_rev(isbn)
    db["comments"] = books.get_review_by_book_id(db["book"]["book"].id)
    #return renderer.render("book", session["usr"], db=db)
    return db["goodreads"]

@app.route("/review/<string:isbn>", methods=["GET", "POST"])
def review(isbn):
    """ function to submit a review for a book receiving books isbn. Linked to from book function """
    log_rt()

    # handle conditions where user is not allowed to post a review
    book_id=books.get_id_by_isbn(isbn)
    if session["usr"].usr_name == None or not books.check_reviewer(session["usr"].usr_id, book_id):
        return renderer.render("review_err", session["usr"])
    if request.method == "POST":
        # check submited review
        if not request.form.get("1st_lang_star") or not request.form.get("1st_lang_star"):
            return renderer.render("review", session["usr"], copy={"review_isbn": isbn}, err="err-review-stars")
        books.add_review(book_id, session["usr"].usr_id, request.form)
        return redirect(url_for("book", isbn=isbn))
    return renderer.render("review", session["usr"], copy={"review_isbn": isbn})

@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    """ function to reply to api queries with book info and averaged review info """
    book = {}
    try:
        # return book info formated into a json file (inside a try catch in case the isbn is not in our database)
        book = books.get_by_isbn(isbn)
        return jsonify({"title": book["book"].title,
                "author": book["book"].author,
                "year": book["book"].year,
                "isbn": book["book"].isbn,
                "review_count": book["review_count"],
                "first_language_average_score": book["first_lang_stars"],
                "second_language_average_score": book["second_lang_stars"]})
    except:
        return jsonify({"error": "not found"}), 404

@app.route("/logout")
def logout():
    """ logs out the user and returns them to the home page.  Retains the users prefered language """
    session["usr"] = Usr(None, session["usr"].pref_lang, 0)
    return redirect(url_for("index"))
