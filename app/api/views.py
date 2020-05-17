from flask_login import login_required,current_user
from flask import request,jsonify,session,current_app
from ..models import Article, Tags
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
        results = tmdb_api.find_subjects(title = request.values.get('title',""),release_year = request.values.get('release_year',None))
        for result in results:
            genres = []
            for genre in result.get('genre_ids'):
                genres.append(Tags.query.filter_by(tmdb_id=genre).first().id)
            result['genres']=genres
        current_app.logger.info(results)
        return jsonify(json.dumps(results))
    except Exception as err:
        current_app.logger.error(err)
        return print(err),500

@api.route('/get-tags')
@login_required
def get_tags():
    """Returns a list of categories formatted for the SELECT2 plugin to use for category/tag dropdown lists."""
    tags = Tags.query.filter(Tags.name.contains(request.values.get('term',''))).all()
    response = {"results":[{"id":tag.id,"text":tag.name,"tmdb_id":tag.tmdb_id} for tag in tags],"pagination":{"more":False}}
    selected_tags_article = Article.query.get(request.values.get('article_id'))
    if selected_tags_article:
        for result in response['results']:
            if Tags.query.get(int(result['id'])) in selected_tags_article.tags.all():
                result['selected'] = True
    return jsonify(json.dumps(response))
