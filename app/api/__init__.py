from flask import Blueprint

api = Blueprint('api',__name__)
from . import views, errors, tmdb_api
from ..models import Permission
