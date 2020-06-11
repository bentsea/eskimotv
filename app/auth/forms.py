from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    user_id = StringField('Email or Username:',
                          render_kw={"autocomplete":"username"},
                          validators=[DataRequired(), Length(1,128)])
    password = PasswordField('Password:',
                             render_kw={"autocomplete":"current-password"},
                             validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email:',
                        render_kw={"autocomplete":"username"},
                        validators=[DataRequired(), Length(1,128),Email()])
    username = StringField('Username:',
                           validators=[DataRequired(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots, or underscores.')])
    password = PasswordField('Password',
                            render_kw={"autocomplete":"new-password"},
                            validators=[DataRequired(), EqualTo('password2', message="Passwords must match.")])
    password2 = PasswordField('Confirm Password',
                              render_kw={"autocomplete":"new-password"},
                              validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class RequestPasswordReset(FlaskForm):
    user_id = StringField('Email or Username',
                          render_kw={"autocomplete":"username"},
                          validators=[DataRequired(), Length(1,128)])
    submit = SubmitField('Request Reset')

class PasswordReset(FlaskForm):
    password = PasswordField('Password:',
                             render_kw={"autocomplete":"new-password"},
                             validators=[DataRequired(),EqualTo('password2',message="Passwords must match.")])
    password2 = PasswordField('Confirm Password:',
                              render_kw={"autocomplete":"new-password"},
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')
