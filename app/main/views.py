from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,ArticleForm
from .. import db
from ..email import send_email
from ..models import User,Role,Article,Permission
from flask_login import login_required,current_user
from ..decorators import admin_required

@main.route('/', methods=['GET','POST'])
def index():
    form=ArticleForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        article = Article(body=form.body.data,author=current_user._get_current_object(),published=datetime.utcnow())
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination=Article.query.order_by(Article.published.desc()).paginate(page,
        per_page=current_app.config['ESKIMOTV_ARTICLES_PER_PAGE'],
        error_out=False)

    articles = pagination.items
    return render_template('main/home.html.j2',form=form,articles=articles,pagination=pagination)

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
