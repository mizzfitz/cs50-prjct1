from flask import render_template, Markup, url_for
import os, json

from databases import Usr

class Renderer:
    def __init__(self, path):
        self.path = path

    def read_dict(self, fname, lang):
        k = open(os.path.join(self.path, "copy", f"{fname}.key"))
        keys = k.readlines()
        k.close()
        t = open(os.path.join(self.path, "copy", f"{fname}{lang}.txt"))
        texts = t.readlines()
        t.close()
        dictionary = {}
        i = 0
        while i < len(keys):
            dictionary[keys[i].strip()] = texts[i].strip()
            i += 1
        return dictionary

    def render_error(self, lang, err):
        if lang == "" or err == "":
            return ""
        errors = self.read_dict("error", lang)
        return f"<p class='error'>{errors.get(err)}</p>"

    def render_usr(self, usr):
        fr = {"login":"se connecter", "sign-up":"créer un compte", "logout":"déconnexion"}
        en = {"login":"login", "sign-up":"create account", "logout":"logout"}
        text = {"fr": fr, "en": en}

        if usr.pref_lang == "":
            return ""

        if usr.usr_name == None:
            return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
        else:
            return Markup(f"<a href=\"{{ url_for('{usr.usr_name}')\">%s</a><a href=\"{url_for('logout')}\">{text[usr.pref_lang]['logout']}</a>") % usr.usr_name

    def get_copy(self, page, lang):
        c = self.read_dict(page, lang)
        c.update(self.read_dict("header", lang))
        return c

    def render(self, page, usr, err="", db={}):
        l = usr.pref_lang
        if l != "":
            l = f".{l}"

        return render_template(f"{page}.html", copy=self.get_copy(page, l), usr=Markup(self.render_usr(usr)), err_txt=Markup(self.render_error(l, err)), db=db)

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
