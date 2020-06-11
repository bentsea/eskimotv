from flask import Blueprint

api = Blueprint('api',__name__)
from . import views
from ..models import Permission
