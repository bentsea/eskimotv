from datetime import datetime,date
from sqlalchemy import func
from flask import render_template, session, redirect, url_for, flash, request, current_app, abort, send_from_directory
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,ArticleForm
from .. import db
from ..email import send_email
from ..models import User,Role,Article,Permission
from flask_login import login_required,current_user
from ..decorators import admin_required
from flask_ckeditor import upload_success, upload_fail
from slugify import slugify
import os

@main.route('/', methods=['GET','POST'])
def index():
    form=ArticleForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        if form.submit.data == True:
            article = Article(title=form.title.data,body=form.body.data,author=current_user._get_current_object(),published=datetime.utcnow())
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('.index'))
        if form.save_draft.data == True:
            article = Article(title=form.body.title,body=form.body.data,author=current_user._get_current_object())
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination=Article.query.order_by(Article.published.desc()).paginate(page,
        per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
        error_out=False)

    articles = pagination.items
    return render_template('main/home.html.j2',form=form,articles=articles,pagination=pagination,time=datetime.utcnow())

@main.route('/user/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()
    articles = user.articles.order_by(Article.published.desc()).all()
    return render_template('main/user.html.j2',user=user, articles=articles)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(user=current_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            changes = False
            if current_user.email != form.email.data:
                token=current_user.generate_email_change_token(form.email.data)
                send_email(form.email.data, "Confirm Email Change","main/email/confirm",user=current_user,new_email=form.email.data,token=token)
                flash('A confirmation has been sent to your chosen new email account.')
            if current_user.last_name != form.last_name.data:
                current_user.last_name = form.last_name.data
                changes=True
            if current_user.first_name != form.first_name.data:
                current_user.first_name = form.first_name.data
                changes=True
            if current_user.about_me != form.about_me.data:
                current_user.about_me = form.about_me.data
                changes=True
            if changes==True:
                db.session.add(current_user._get_current_object())
                db.session.commit()
                flash('Your changes have been saved.')
            else:
                flash('No edits were made.')
            return redirect(url_for('.profile',id=current_user.id))
        else:
            if form.cancel.data:
                flash('No edits were made to your account.')
                return redirect(url_for('.profile',id=current_user.id))
            else:
                for error in form.errors:
                    flash(form.errors[error][0])
                return render_template('main/edit_user.html.j2',user=current_user,form=form)
    form.email.data = current_user.email
    form.last_name.data = current_user.last_name
    form.first_name.data = current_user.first_name
    form.about_me.data = current_user.about_me
    return render_template('main/edit_user.html.j2',user=current_user,form=form)


@main.route('/confirm_email_change/<token>')
@login_required
def confirm_email_change(token):
    if current_user.change_email(token):
        flash('Your email has been successfully updated.')
        db.session.commit()
        return redirect(url_for('.profile',id=current_user.id))
    else:
        flash('This email confirmation link is expired or invalid. Please try again.')
        return redirect(url_for('.profile',id=current_user.id))

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            user.email = form.email.data
            user.username = form.username.data
            user.confirmed = form.confirmed.data
            user.role = Role.query.get(form.role.data)
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.about_me = form.about_me.data
            db.session.add(user)
            db.session.commit()
            flash('The profile has been updated.')
            return redirect(url_for('.profile',id=user.id))
        else:
            if form.cancel.data:
                flash('No edits were made to your account.')
                return redirect(url_for('.profile',id=user.id))
            for error in form.errors:
                flash(form.errors[error])
            return render_template('main/edit_user.html.j2',form=form, user=user)
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.about_me.data = user.about_me
    return render_template('main/edit_user.html.j2', form=form, user=user)


@main.route('/images',methods=['GET','POST'])
@login_required
def upload_images():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension.lower() not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    path = os.path.join(current_app.config['FLASKFILEMANAGER_FILE_PATH'],current_user.username)
    filepath = os.path.join(path,f.filename)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.isfile(filepath):
        return upload_fail("File with that name already exists.")
    f.save(filepath)
    url = url_for('static', filename="uploads/{}/{}".format(current_user.username,f.filename))
    return upload_success(url=url)  # return upload_success call


@main.route('/articles/<string:title_slug>')
def article(title_slug):
    article = Article.query.filter_by(title_slug=title_slug).first_or_404()
    if article.published > datetime.utcnow() and not current_user.is_administrator():
        abort(404)
    return render_template('main/article.html.j2',articles=[article])

@main.route('/articles/id/<int:id>')
def article_by_id(id):
    article = Article.query.get_or_404(id)
    return render_template('main/article.html.j2',articles=[article])

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if current_user != article.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = ArticleForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if Article.query.filter_by(title_slug=slugify(form.title.data)).first() and article.title != form.title.data:
                    flash("Your title is too similar to an existing article.")
                    return render_template('main/edit_article.html.j2',form=form,article=article)
                article.body = form.body.data
                article.title = form.title.data
                article.draft = None
                article.published = form.publish_date.data
                db.session.add(article)
                db.session.commit()
                flash('The article has been successfully updated.')
                return redirect(url_for('main.article_by_id',id=id))
            if form.save_draft.data:
                article.draft_title = form.title.data
                article.draft = form.body.data
                db.session.add(article)
                db.session.commit()
                flash("Edits saved as draft.")
                return redirect(url_for('main.article_by_id',id = article.id))
    if request.args.get('edit') == 'draft':
        form.title.data = article.draft_title
        form.body.data = article.draft
    else:
        form.title.data = article.title
        form.body.data = article.body
    if article.published:
        form.publish_date.data = article.published
    else:
        form.publish_date.data = datetime.utcnow()
    return render_template('main/edit_article.html.j2',form=form,article=article)

@main.route('/discard_draft')
@login_required
def discard_draft():
    article = Article.query.get_or_404(request.args.get('id'))
    if current_user == article.author or current_user.can(Permission.EDIT):
        article.draft = None
        article.draft_title = None
        db.session.add(article)
        db.session.commit()
        flash('Draft discarded.')
        return redirect(url_for('main.article',title_slug=article.title_slug))
    else:
        flash("You don't have permission to discard this user's drafts.")
        return redirect(url_for('main.article',title_slug=article.title_slug))
