from flask import render_template, request, jsonify
from . import main

#Define 404 error handling.
@main.app_errorhandler(404)
def not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template("errors/404.html.j2"),404
