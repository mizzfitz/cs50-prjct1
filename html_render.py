from flask import render_template, Markup, url_for
import os, json

from databases import Usr

NAME = "BiLingue"

def render_usr(usr):
    fr = {"login":"Connexion", "sign-up":"S'enregistrer"}
    en = {"login":"Login", "sign-up":"Create Account"}
    bi = {"login":"Login/Connexion", "sign-up":"Create Account/S'enregistrer"}
    text = {"fr": fr, "en": en, "": bi}

    if usr.usr_name == None:
        return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
    else:
        return Markup(f"<a href=\"{{ url_for('{usr.usr_name}')\">%s</a>") % usr.usr_name

def render(path, page, usr):
    l = usr.pref_lang
    if l != "":
        l = f".{l}"
    k = open(os.path.join(path, "copy", f"{page}.key"))
    keys = k.readlines()
    k.close()
    t = open(os.path.join(path, "copy", f"{page}{l}.txt"))
    texts = t.readlines()
    t.close()
    copy = {}
    i = 0
    while i < len(keys):
        copy[keys[i].strip()] = texts[i].strip()
        i += 1

    return render_template(f"{page}.html", name=NAME, copy=copy, usr=Markup(render_usr(usr)))

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
