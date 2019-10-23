from flask import render_template
import os, json

NAME = "BiLingue"

def render(path, page, usr):
    f = open(os.path.join(path, "copy", f"{page}.json"))
    copy = json.loads(f.read())
    
    return render_template(f"{page}.html", name=NAME, copy=copy, usr=usr)
