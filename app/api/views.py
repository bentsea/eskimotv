from flask_login import login_required,current_user
from flask import request,jsonify,session
import base64
import json
from . import api
from . import tmdb_api
from flask_login import login_required,current_user


@api.route('/get_backdrops')
@login_required
def get_backdrops():
    try:
        return jsonify(json.dumps(tmdb_api.get_backdrops(request.args.get('media_type'),request.args.get('id'))))
    except Exception as err:
        return str(err), 500

@api.route('/test')
def this_test():
    try:
        api_key = request.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ','',1)
            try:
                api_key = base64.b64decode(api_key)
            except TypeError:
                pass
        return api_key
    except Exception as err:
        return str(err),500
