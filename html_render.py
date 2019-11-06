from flask import render_template, Markup, url_for
import os, json

from databases import Usr

class Renderer:
    """ the main class for rendering html """

    def __init__(self, path):
        """ stores the path to the copy directory.  Takes as input the path the the parent directory """
        self.path = os.path.join(path, "copy")

    def read_dict(self, fname, lang):
        """ function for creating a dictionary of ui keys value pairs based on a file name and a language """

        k = open(os.path.join(self.path, f"{fname}.key"))
        keys = k.readlines()
        k.close()
        t = open(os.path.join(self.path, f"{fname}{lang}.txt"))
        texts = t.readlines()
        t.close()
        dictionary = {}
        i = 0
        while i < len(keys):
            dictionary[keys[i].strip()] = texts[i].strip()
            i += 1
        return dictionary

    def render_error(self, lang, err):
        """ function for creating error message html (including tags) based on an error message.
        This function does not include any user generated content so it is safely rendered without html escaping in the main render function """
        if lang == "" or err == "":
            return ""
        errors = self.read_dict("error", lang)
        return f"<p class='error'>{errors.get(err)}</p>"

    def render_usr(self, usr):
        """ function for creating html (including tags) for login and sign up or user name and logout ui based on whether a user is signed in.
        The output of this function is not escaped in the final render function so any user generated content has to be escaped within the function """

        fr = {"login":"se connecter", "sign-up":"créer un compte", "logout":"déconnexion"}
        en = {"login":"login", "sign-up":"create account", "logout":"logout"}
        text = {"fr": fr, "en": en}

        if usr.pref_lang == "":
            return ""

        if usr.usr_name == None:
            return f"<a href=\"{url_for('login')}\">{text[usr.pref_lang]['login']}</a><a href=\"{url_for('sign_up')}\">{text[usr.pref_lang]['sign-up']}</a>"
        else:
            # user name is user generated content so we escape it using Markup
            return Markup(f"<a href=''>%s</a><a href=\"{url_for('logout')}\">{text[usr.pref_lang]['logout']}</a>") % usr.usr_name

    def get_copy(self, page, lang):
        """ function for generating a dictionary of copy for a given page based on a page name and a langueage """
        c = self.read_dict(page, lang)
        c.update(self.read_dict("header", lang))
        return c

    def render(self, page, usr, copy={}, err="", db={}):
        """ the main rendering function """

        # format a string representing users prefered language to send to functions for building ui and copy data
        l = usr.pref_lang
        if l != "":
            l = f".{l}"

        # add values generated within this object to any directly given bits of copy (allows the main program to generate bits of copy while mosty relying on files in the copy directory to generate copy)
        copy.update(self.get_copy(page, l))

        # return a rendered jinja template.  Results of render_usr() and render_error() are marked as safe bacause we need them to render html tags
        return render_template(f"{page}.html", copy=copy, usr=Markup(self.render_usr(usr)), err_txt=Markup(self.render_error(l, err)), db=db)

if __name__ == "__main__":
    print("This module is intended for use within a specific flask app")
