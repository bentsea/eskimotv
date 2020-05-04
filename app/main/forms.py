from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, HiddenField
from wtforms.fields.html5 import DateTimeField
from flask_ckeditor import CKEditorField
from sqlalchemy import func
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from slugify import slugify
from ..models import Role,User,ArticleType

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
                             for role in Role.query.order_by(Role.id).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ArticleForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,128)])
    body = CKEditorField('Article Body:', validators=[DataRequired()])
    publish_date = DateTimeField('Update published date:')
    submit = SubmitField('Publish')
    save_draft = SubmitField('Save Draft')

class NewArticle(FlaskForm):
    title = StringField('Article Title:',validators=[DataRequired(),Length(1,128)])
    article_type = SelectField('Article Type:', coerce=int)
    subject_title = HiddenField('Subject Title')
    subject_image = HiddenField('Subject Image')
    tmdb_id = HiddenField('Subject ID')
    subject_type = HiddenField('Subject Type')
    subject_selected = HiddenField('Subject Selected',validators=[DataRequired()])
    cover_image_file = FileField('Use a Local File')
    cover_image_url = StringField('Use an Image From Online',render_kw={"placeholder": "Image URL"})
    create_draft = SubmitField('Create Draft')

    def __init__(self, *args, **kwargs):
        super(NewArticle, self).__init__(*args, **kwargs)
        self.article_type.choices = [(type.id, type.name)
                             for type in ArticleType.query.order_by(ArticleType.id).all()]
