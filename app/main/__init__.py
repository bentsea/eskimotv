from flask import Blueprint

main = Blueprint('main',__name__)
from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    from flask import render_template_string,render_template
    return dict(Permission=Permission,render_template_string=render_template_string,render_template=render_template)
