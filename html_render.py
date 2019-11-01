from flask import render_template, Markup, url_for
import os, json

from databases import Usr

NAME = "BiLingue"

class Renderer():
    def __init__(self, name):
        self.NAME = name

    def render_error(self, path, err, lang):
        k = open(os.path.join(path, "copy", "error.key"))
        keys = k.readlines()
        k.close()
        t = open(os.path.join(path, "copy", f"error{lang}.txt"))
        texts = t.readlines()
        t.close()
        errors = {}
        i = 0
        while i < len(keys):
            errors[keys[i].strip()] = texts[i].strip()
            i += 1
        return f"<p class='error'>{errors.get(err)}</p>"

    def render_usr(usr):
        fr = {"login":"se connecter", "sign-up":"créer un compte", "logout":"déconnexion"}
        en = {"login":"login", "sign-up":"create account", "logout":"logout"}
        text = {"fr": fr, "en": en}

        if usr.pref_lang == "":
            return ""

        if usr.usr_name == None:
            return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
        else:
            html = Markup(f"<a href=\"{{ url_for('{usr.usr_name}')\">%s</a>") % usr.usr_name
            html = f"{html}<a href=\"{url_for('logout')}\">{text[usr.pref_lang]['logout']}</a>"
            return html

    def render(self, path, page, usr, err=""):
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
            err = self.render_error(path, err, l)

        return render_template(f"{page}.html", name=self.NAME, copy=copy, usr=Markup(self.render_usr(usr)), err_txt=Markup(err), search=search(usr.pref_lang))

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
