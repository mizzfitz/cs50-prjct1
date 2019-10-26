from flask import render_template, Markup, url_for
import os, json

from databases import Usr

NAME = "BiLingue"

def render_error(path, err, lang):
    e = ["no-login", "dito-usr-name", "unknown"]
    f = open(os.path.join(path, "copy" f"error{lang}.txt"))
    texts = f.readlines()
    f.close()
    i = 0
    while i < len(e):
        errors[e[i]] = texts[i].strip()
    return f"<p class='error'>{errors.get(err)}</p>"

def render_usr(usr):
    fr = {"login":"Connexion", "sign-up":"S'enregistrer"}
    en = {"login":"Login", "sign-up":"Create Account"}
    bi = {"login":"Login/Connexion", "sign-up":"Create Account/S'enregistrer"}
    text = {"fr": fr, "en": en, "": bi}

    if usr.usr_name == None:
        return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
    else:
        return Markup(f"<a href=\"{{ url_for('{usr.usr_name}')\">%s</a>") % usr.usr_name

def render(path, page, usr, err=""):
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

    if err != "":
        err = render_error(path, err, l)

    return render_template(f"{page}.html", name=NAME, copy=copy, usr=Markup(render_usr(usr)), err_txt=Markup(err))

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
