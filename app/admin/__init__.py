from flask import Blueprint

admin = Blueprint('admin',__name__)
from . import views, errors, forms, files
from ..models import Permission

@admin.app_context_processor
def inject_permissions():
    from flask import render_template_string,render_template
    return dict(Permission=Permission,render_template_string=render_template_string,render_template=render_template)
