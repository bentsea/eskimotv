from datetime import datetime,date
from flask import render_template, session, redirect, url_for, flash, request, current_app, abort
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
    pagination=Article.query.filter_by(published=True).order_by(Article.publish_date.desc()).paginate(page,
        per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
        error_out=False)

    # articles = pagination.items
    articles = [article for article in Article.query.all()[:30] if article.published]
    all_articles={}
    for type in ArticleType.query.all():
        all_articles[type.name] = [ article for article in type.articles.order_by(Article.publish_date.desc()).all()[:15] if article.published]
    return render_template('main/home.html.j2',articles=articles,all_articles=all_articles,pagination=pagination,time=datetime.utcnow())

@main.route('/articles/<string:title_slug>')
def article(title_slug):
    article = Article.query.filter_by(title_slug=title_slug).first_or_404()
    if not article.published and not current_user.is_administrator() and not current_user.can(Permission.EDIT) and not current_user == article.author:
        abort(404)
    return render_template('main/article.html.j2',article=article)
