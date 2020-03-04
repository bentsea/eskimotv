from flask_login import login_required,current_user
from flask import request
import json
from . import api
from . import tmdb_api
from flask_login import login_required,current_user
#import tmdb_api


@api.route('/get_backdrops')
@login_required
def get_backdrops():
    try:
        return tmdb_api.get_backdrops(request.args.get('media_type'),request.args.get('id'))
    except Exception as err:
        return str(err), 500
