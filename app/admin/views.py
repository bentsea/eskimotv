from datetime import datetime,date
from flask import render_template, get_template_attribute, session, redirect, url_for, flash, request, current_app, abort, send_from_directory,jsonify
import json
from .. import db
from ..api import tmdb_api
from ..email import send_email
from . import admin
from sqlalchemy import func
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,ArticleForm,NewArticle
from slugify import slugify
from ..models import User,Role,Article,Permission,ArticleType,Tags,CreativeWork,Person
from flask_login import login_required,current_user
from ..decorators import admin_required
from flask_ckeditor import upload_success, upload_fail

def add_new_creative_work(tmdb_id,media_type):
    creative_work = CreativeWork.query.filter_by(tmdb_id=tmdb_id).first()
    if not creative_work:
        creative_work_data = tmdb_api.get_creative_work(tmdb_id,media_type)
        creative_work = CreativeWork(
            type=creative_work_data['CreativeWork']['type'],
            name=creative_work_data['CreativeWork']['name'],
            same_as=creative_work_data['CreativeWork']['same_as'],
            tmdb_id=creative_work_data['CreativeWork']['tmdb_id'],
            image=creative_work_data['CreativeWork']['image'],
            date_published=creative_work_data['CreativeWork']['date_published'])
        db.session.add(creative_work)
        db.session.commit()
        for person_info in creative_work_data['Person']:
            person = Person.query.filter_by(tmdb_id=person_info['tmdb_id']).first()
            if not person:
                person = Person(tmdb_id=person_info['tmdb_id'],name=person_info['name'])
            try:
                db.session.add(person)
                db.session.commit()
            except:
                db.session.rollback()
            if person not in creative_work.directed_by.all():
                creative_work.directed_by.append(person)
                try:
                    db.session.add(creative_work)
                    db.session.commit()
                except:
                    db.session.rollback()
    return creative_work

@admin.route('/user/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()
    articles = user.articles.order_by(Article.publish_date.desc()).all()
    return render_template('main/user.html.j2',user=user, articles=articles)

@admin.route('/edit-profile',methods=['GET','POST'])
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

@admin.route('/confirm_email_change/<token>')
@login_required
def confirm_email_change(token):
    if current_user.change_email(token):
        flash('Your email has been successfully updated.')
        db.session.commit()
        return redirect(url_for('.profile',id=current_user.id))
    else:
        flash('This email confirmation link is expired or invalid. Please try again.')
        return redirect(url_for('.profile',id=current_user.id))

@admin.route('/edit-profile/<int:id>',methods=['GET','POST'])
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


@admin.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if current_user != article.author and not current_user.can(Permission.EDIT):
        abort(403)
    if article.published and not current_user.can(Permission.PUBLISH):
        flash('You do not have permissions to edit published articles. Please contact a Publisher for assistance.')
        return redirect(article.url)
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
                article.publish_date = form.publish_date.data
                article.is_published = True
                db.session.add(article)
                db.session.commit()
                for tag_id in form.tags_selector.data:
                    tag = Tags.query.get(tag_id)
                    if tag not in article.tags.all():
                        try:
                            article.tags.append(tag)
                            db.session.add(article)
                            db.session.commit()
                        except:
                            current_app.logger.info('Error')
                            db.session.rollback()
                            continue
                for tag in article.tags.all():
                    if str(tag.id) not in form.tags_selector.data:
                        article.tags.remove(tag)
                        db.session.add(article)
                        db.session.commit()
                flash('The article has been successfully published.')
                return redirect(article.url)
            if form.save_draft.data:
                article.draft_title = form.title.data
                article.draft = form.body.data
                db.session.add(article)
                db.session.commit()
                for tag_id in form.tags_selector.data:
                    tag = Tags.query.get(tag_id)
                    if tag not in article.tags.all():
                        try:
                            article.tags.append(tag)
                            db.session.add(article)
                            db.session.commit()
                        except:
                            current_app.logger.info('Error')
                            db.session.rollback()
                            continue
                for tag in article.tags.all():
                    if str(tag.id) not in form.tags_selector.data:
                        article.tags.remove(tag)
                        db.session.add(article)
                        db.session.commit()
                flash("Draft has been succesfully updated.")
                return redirect(article.url)
        else:
            for fieldName, errorMessages in form.errors.items():
                for error in errorMessages:
                    flash(f'{fieldName} {error}')
    if request.args.get('edit') == 'draft':
        form.title.data = article.draft_title
        form.body.data = article.draft
    else:
        form.title.data = article.title
        form.body.data = article.body
    if article.published:
        form.publish_date.data = article.publish_date
    else:
        form.publish_date.data = datetime.utcnow()
    return render_template('main/edit_article.html.j2',form=form,article=article)

@admin.route('/discard_draft')
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

@admin.route('/unpublish', methods=["GET","POST"])
@login_required
def unpublish():
    article_id = request.values.get('article_id')
    if article_id:
        article = Article.query.get_or_404(article_id)
        article.is_published = False
        db.session.add(article)
        db.session.commit()
        flash('This article has been removed from publication.')
        return redirect(article.url)
    else:
        flash('You are toying with powers beyond your comprehension. Do not try that again.')
        flash('Your activity has been reported.')
        return redirect(url_for('main.index'))

@admin.route('/new_article/',methods=["GET","POST"])
@login_required
def new_article():
    if not current_user.can(Permission.WRITE):
        abort(403)
    form = NewArticle()
    if request.method == "POST":
        return render_template('main/new_article.html.j2',form=form)
        if form.validate_on_submit():
            new_article = Article(title=form.title.data,
                publish_date=datetime.now(),
                author=current_user,
                type=ArticleType.query.get(form.article_type.data))
            if form.subject_selected.data != "None":
                subject = CreativeWork.query.filter_by(tmdb_id=form.tmdb_id.data).first()
                if not subject:
                    subject = add_new_creative_work(form.tmdb_id.data,form.subject_type.data)
    return render_template('main/new_article.html.j2',form=form)


@admin.route('/change_cover/<int:id>',methods=['GET','POST'])
@login_required
def change_cover(id):
    article = Article.query.get_or_404(request.args.get('id'))
    if (article.published and current_user.can(Permission.PUBLISH)) or (not article.published and (current_user == article.author or current_user.can(Permission.EDIT))):
        flash("You have permission to edit this article's image, but that function doesn't work right now.")
        return redirect(url_for('main.article',title_slug=article.title_slug))
    else:
        if article.published:
            flash("You don't have permission to change the image on published articles.")
            return redirect(url_for('main.article',title_slug=article.title_slug))
        else:
            flash("You don't have permission to edit this article.")
            return redirect(url_for('main.article',title_slug=article.title_slug))


@admin.route('/images',methods=['GET','POST'])
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
