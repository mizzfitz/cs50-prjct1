from flask import render_template, Markup, url_for
import os, json

from databases import Usr

def read_dict(path, fname, lang):
    k = open(os.path.join(path, "copy", f"{fname}.key"))
    keys = k.readlines()
    k.close()
    t = open(os.path.join(path, "copy", f"{fname}{lang}.txt"))
    texts = t.readlines()
    t.close()
    dictionary = {}
    i = 0
    while i < len(keys):
        dictionary[keys[i].strip()] = texts[i].strip()
        i += 1
    return dictionary

def render_error(path, lang, err):
    if lang == "" or err == "":
        return ""
    errors = read_dict(path, "error", lang)
    return f"<p class='error'>{errors.get(err)}</p>"

def render_usr(usr):
    fr = {"login":"se connecter", "sign-up":"créer un compte", "logout":"déconnexion"}
    en = {"login":"login", "sign-up":"create account", "logout":"logout"}
    text = {"fr": fr, "en": en}

    #if usr.pref_lang == "":
        #return ""

    if usr.usr_name == None:
        return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
    else:
        return Markup(f"<a href=\"{{ url_for('{usr.usr_name}')\">%s</a><a href=\"{url_for('logout')}\">{text[usr.pref_lang]['logout']}</a>") % usr.usr_name

def get_copy(path, page, lang):
    c = read_dict(path, page, lang)
    c.update(read_dict(path, "header", lang))
    return c

def render(path, page, usr, err=""):
    l = usr.pref_lang
    if l != "":
        l = f".{l}"

    return render_template(f"{page}.html", copy=get_copy(path, page, l), usr=Markup(render_usr(usr)), err_txt=Markup(render_error(path, l, err)))

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
