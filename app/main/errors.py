from flask import render_template
from . import main

#Define 404 error handling.
@main.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html.j2"),404
