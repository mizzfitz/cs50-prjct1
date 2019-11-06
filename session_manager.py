import requests

from flask import request, session, redirect, url_for
from databases import Usr

def resume_sess():
    """ function to return user to where they were prior to login/sign_up or language selection """
    if session.get("req_log") is None:
        return redirect(url_for("index"))
    while session["req_log"][-1] == request.url:
        session["req_log"].pop()
        if len(session["req_log"]) < 1:
            session["req_log"] = [url_for("index")]
            return redirect(url_for("index"))
    return redirect(session["req_log"][-1])

def log_rt():
    """ function to log the users location within the app for use in resume_sess() """
    if session.get("req_log") is None:
        session["req_log"] = [request.url]
    else:
        session["req_log"].append(request.url)
        while len(session["req_log"]) > 5:
            session["req_log"].pop(0)

def goodreads_rev(isbn):
    """ function for getting review info from goodreads api """
    isbn = isbn.strip()
    r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O8fo8CINWE0gI5EgY1GaUw", "isbns": isbn})
    try:
        return r.json()["books"][0]
    except:
        return None

def check_lang():
    """ function to check if the user has selected a prefered language and redirect them to the language selection if they have not """
    if session.get("usr") is None:
        session["usr"] = Usr(None)
        return True
    elif session["usr"].pref_lang == "":
        return True
    else:
        return False

