from flask import render_template

def render(path):
    index = {"text1":"This is the first text block", "text2":"This is the second text block"}
    return render_template("index.html", index=index)
