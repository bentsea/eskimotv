from datetime import datetime,date
from flask import render_template, session, redirect, url_for, flash, request, current_app, abort, make_response
from . import main
from .. import db
from ..models import User,Role,Article,Permission,ArticleType,Tags,CreativeWork
from flask_login import login_required,current_user
from ..decorators import admin_required

import os

@main.route('/', methods=['GET','POST'])
def index():
    # if current_user.can(Permission.WRITE) and form.validate_on_submit():
    #     if form.submit.data == True:
    #         article = Article(title=form.title.data,body=form.body.data,author=current_user._get_current_object(),publish_date=datetime.utcnow())
    #         db.session.add(article)
    #         db.session.commit()
    #         return redirect(url_for('.index'))
    #     if form.save_draft.data == True:
    #         article = Article(title=form.body.title,body=form.body.data,author=current_user._get_current_object())
    #         db.session.add(article)
    #         db.session.commit()
    #         return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination=Article.query.order_by(Article.publish_date.desc()).paginate(page,
        per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
        error_out=False)

    # articles = pagination.items
    articles = Article.query.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).all()
    all_articles={}
    for type in ArticleType.query.all():
        all_articles[type.name] = type.articles.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).all()
    return render_template('main/home.html.j2',articles=articles,all_articles=all_articles,pagination=pagination,time=datetime.utcnow())

@main.route('/articles/<string:title_slug>')
def article(title_slug):
    article = Article.query.filter_by(title_slug=title_slug).first_or_404()
    if not article.published and not current_user.is_administrator() and not current_user.can(Permission.EDIT) and not current_user == article.author:
        abort(404)
    return render_template('main/article.html.j2',article=article)

@main.route('/user/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()
    def query_for_user():
        if current_user == user:
            return user.articles
        else:
            return user.articles.filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True)
    def query_for_requests_to_publish():
        if current_user.can(Permission.PUBLISH):
            return Article.query.filter_by(request_to_publish=True)
        else:
            abort(403,description="You don't have permission to publish.")
    def query_for_all_unpublished():
        if current_user.can(Permission.PUBLISH):
            return Article.query.filter((Article.publish_date >= datetime.utcnow()) | (Article.is_published==False))
    display_options = {
        'none':query_for_user,
        "waiting_for_publication":query_for_requests_to_publish,
        "unpublished":query_for_all_unpublished
    }
    display = 'none'
    if current_user.is_authenticated:
        display = request.cookies.get('display','none')
        if current_user.id != id and display == "followed":
            display = 'none'
    query = display_options[display]()
    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Article.publish_date.desc()).paginate(page,
        per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    return render_template('main/user.html.j2',user=user, articles=articles,display=display,pagination=pagination)

@main.route('/toggle_user_display')
def toggle_user_display():
    response = make_response(redirect(url_for('main.profile',id=request.args.get('user_id'))))
    response.set_cookie('display',request.args.get('display','none'),max_age=30*24*60*60)
    return response


@main.route('/reviews')
def reviews():
        page = request.args.get('page',1,type=int)
        type = ArticleType.query.filter_by(name="Review").first()
        pagination=type.articles.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).paginate(page,
            per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('main/archive_template.html.j2',articles=articles,pagination=pagination,time=datetime.utcnow())

@main.route('/editorials')
def editorials():
        page = request.args.get('page',1,type=int)
        type = ArticleType.query.filter_by(name="Editorial").first()
        pagination=type.articles.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).paginate(page,
            per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('main/archive_template.html.j2',articles=articles,pagination=pagination,time=datetime.utcnow())

@main.route('/news')
def news():
        page = request.args.get('page',1,type=int)
        type = ArticleType.query.filter_by(name="News").first()
        pagination=type.articles.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).paginate(page,
            per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('main/archive_template.html.j2',articles=articles,pagination=pagination,time=datetime.utcnow())

@main.route('/archive')
def archive():
        page = request.args.get('page',1,type=int)
        pagination=Article.query.order_by(Article.publish_date.desc()).filter(Article.publish_date <= datetime.utcnow(),Article.is_published==True).paginate(page,
            per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        return render_template('main/archive_template.html.j2',articles=articles,pagination=pagination,time=datetime.utcnow())

@main.route('/feed.xml')
def rss_feed():
    return None
