from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from . import auth
from ..models import User
from datetime import datetime
from .. import db
from ..email import send_email
from .forms import LoginForm,RegistrationForm,RequestPasswordReset,PasswordReset
import base64

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html.j2')

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.user_id.data).first() or User.query.filter_by(username=form.user_id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html.j2', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "Confirm Your Account","auth/email/confirm",user=user,token=token)
        flash('A confirmation email has been sent to the address you registered with.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html.j2',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    flash('Please log in to complete confirmation.')
    if current_user.confirmed:
        flash('This account is already confirmed.')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,"Confirm Your Account","auth/email/confirm",user=current_user,token=token)
    flash('A new confirmation email has been sent to your address.')
    return redirect(url_for('main.index'))

@auth.route('/reset',methods=['GET','POST'])
def request_reset_password():
    form = RequestPasswordReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.user_id.data).first() or User.query.filter_by(username=form.user_id.data).first()
        if user is not None:
            token = user.generate_reset_token()
            send_email(user.email, "Password Reset Request","auth/email/reset",user=user,token=token)
        flash('A reset request has been sent to the email address of the account.')
        return redirect(url_for('main.index'))
    return render_template('auth/request_password_reset.html.j2',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def reset_password(token):
    user = User.check_reset_request(token)
    form = PasswordReset()
    if user == False:
        flash('This reset request has expired or is invalid.')
        return redirect('main.index')
    if form.validate_on_submit():
        user.password = form.password.data
        flash('Your password has been successfully reset.')
        return redirect(url_for('auth.login'))
    return render_template("auth/password_reset.html.j2",form=form, user=user)
