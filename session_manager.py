from flask import request, session, redirect, url_for
from databases import Usr

def resume_sess():
    if session.get("req_log") is None or session.get("req_log") == request.endpoint:
        return redirect(url_for("index"))
    else:
        return redirect(url_for(session["req_log"]))

def log_rt():
    session["req_log"] = request.endpoint

def check_lang():
    if session.get("usr") is None:
        session["usr"] = Usr(None)
        return True
    elif session["usr"].pref_lang == "":
        return True
    else:
        return False

