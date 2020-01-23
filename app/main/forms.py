from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role,User

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(0,128), Email()])
    first_name = StringField('First Name', validators=[Length(0,64)])
    last_name = StringField('Last Name', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('That email is already registered.')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    first_name = StringField('First name', validators=[Length(0, 64)])
    last_name = StringField('Last name',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ArticleForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,64)])
    body = CKEditorField('Article Body:', validators=[DataRequired()])
    submit = SubmitField('Publish')
    save_draft = SubmitField('Save Draft')
