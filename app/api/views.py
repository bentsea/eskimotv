from flask_login import login_required,current_user
from flask import request,jsonify,session,current_app
from ..models import Tags
import base64
import json
from . import api
from . import tmdb_api
from flask_login import login_required,current_user


@api.route('/get_backdrops')
@login_required
def get_backdrops():
    """When provided with a TMDB id as 'id' and the media type of the desired id, this returns a list of backdrop images for that object from TMDB if they are present."""
    try:
        return jsonify(json.dumps(tmdb_api.get_backdrops(request.args.get('media_type'),request.args.get('id'))))
    except Exception as err:
        return str(err), 500

@api.route('/tmdb_search',methods=["GET","POST"])
@login_required
def tmdb_search():
    """Returns a list of results from TMDB based on the specified query values. 'title' is required and 'release_year' can be specified to narrow results."""
    try:
        return jsonify(json.dumps(tmdb_api.find_subjects(title = request.values.get('title',""),release_year = request.values.get('release_year',None))))
    except Exception as err:
        return print(err),500

@api.route('/get-tags')
@login_required
def get_tags():
    """Returns a list of categories formatted for the SELECT2 plugin to use for category/tag dropdown lists."""
    tags = Tags.query.filter(Tags.name.contains(request.values.get('term',''))).all()
    response = {"results":[{"id":tag.id,"text":tag.name,"tmdb_id":tag.tmdb_id} for tag in tags],"pagination":{"more":False}}
    return jsonify(json.dumps(response))
