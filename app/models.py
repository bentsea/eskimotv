from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, render_template_string,url_for
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime,date
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import slugify
import hashlib
import bleach

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    EDIT = 8
    PUBLISH = 16
    ADMIN = 32

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return f'<Role {self.name}>'

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT],
            'Writer': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Editor': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.EDIT],
            'Publisher': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.EDIT, Permission.PUBLISH],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.EDIT, Permission.PUBLISH, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(128),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    first_name=db.Column(db.String(64))
    last_name=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    articles = db.relationship('Article',backref='author',lazy="dynamic")
    followed = db.relationship('Follow',
                foreign_keys=[Follow.follower_id],
                backref=db.backref('follower', lazy='joined'),
                lazy='dynamic',
                cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                foreign_keys=[Follow.followed_id],
                backref=db.backref('followed', lazy='joined'),
                lazy='dynamic',
                cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ESKIMOTV_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,
            hash=hash,
            size=size,
            default=default,
            rating=rating)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'reset':self.id}).decode('utf-8')

    @staticmethod
    def check_reset_request(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        return user

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class ArticleType(db.Model):
    __tablename__="article_type"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),index=True)
    articles = db.relationship('Article',backref='type',lazy='dynamic')

    def __repr__(self):
        return '<{} Article>'.format(self.name)

    @staticmethod
    def insert_article_types():
        types = ["Review","Editorial","News"]
        for t in types:
            type = ArticleType.query.filter_by(name=t).first()
            if type == None:
                type = ArticleType(name=t)
            db.session.add(type)
        db.session.commit()


article_tags =db.Table("article_tags",
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    article_type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'))
    image = db.Column(db.String(128))
    title = db.Column(db.String(128),index=True)
    title_slug = db.Column(db.String(64),index=True)
    draft_title = db.Column(db.String(64))
    body_html = db.Column(db.Text)
    body = db.Column(db.Text)
    draft = db.Column(db.Text)
    blurb = db.Column(db.String(256))
    youtube = db.Column(db.String(64))
    final_verdict = db.Column(db.String(256))
    rating = db.Column(db.Integer,index=True)
    letter_rating = db.Column(db.String(3))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, index=True)
    is_published = db.Column(db.Boolean,index=True,default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('creative_works.id'))
    request_to_publish = db.Column(db.Boolean,index=True)
    tags = db.relationship('Tags',secondary=article_tags,backref=db.backref('articles',lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Article {}>'.format(self.title)

    @hybrid_property
    def published(self):
        """Returns true if the publish date is at or before the current time and is_published is true."""
        return self.is_published and self.publish_date <= datetime.now()

    @property
    def url(self):
        """Return the canonical URL for the article."""
        return url_for('main.article', title_slug = self.title_slug,_external=True)

    @property
    def related_articles(self, count=7):
        """Returns a list of articles that share tags in common ranked in descending order."""
        article_id = self.id

        sub_stmt = db.session.query(article_tags.c.tag_id)\
            .filter(article_tags.c.article_id==article_id)

        query = db.session.query(Article.id,
            func.count(article_tags.c.tag_id).label('total'),
            func.group_concat(article_tags.c.tag_id).label('related_tags'))\
            .filter(Article.id!=article_id)\
            .filter(article_tags.c.tag_id.in_(sub_stmt))\
            .filter(article_tags.c.article_id==Article.id)\
            .group_by(Article.id)\
            .order_by(func.count(article_tags.c.tag_id).desc()).order_by(Article.publish_date.desc()).all()

        return [Article.query.get(article[0]) for article in query[:count]]

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul','img','figure','figcaption',
                        'h1', 'h2', 'h3','h4', 'p']
        allowed_attr = ['alt','height','width','src','class']
        target.body_html = bleach.linkify(bleach.clean(render_template_string(value),tags=allowed_tags, attributes=allowed_attr, strip=True))

    @staticmethod
    def on_changed_rating(target,value,oldvalue,initiator):
        def get_letter_grade(grade):
            score_range = {"A+":99,"A":94,"A-":89,"B+":88,"B":84,"B-":79,"C+":78,"C":74,"C-":69,"D+":59,"D":39,"D-":19,"F":0}
            for letter_grade,minimum in score_range:
                if grade >= minimum:
                    return letter_grade
        target.letter_rating = get_letter_grade(value)

    @staticmethod
    def on_changed_title(target,value,oldvalue,initiator):
        target.title_slug = slugify(value)

class Tags(db.Model):
    __tablename__="tags"
    id = db.Column(db.Integer,primary_key=True,index=True)
    tmdb_id = db.Column(db.Integer,unique=True,index=True)
    name = db.Column(db.String(64),unique=True,index=True)

    def __repr__(self):
        return f'<Tag: {self.name}>'


director_relationship = db.Table("directs",
    db.Column('directed_id', db.Integer, db.ForeignKey('creative_works.id')),
    db.Column('director_id', db.Integer, db.ForeignKey('people.id')))

class CreativeWork(db.Model):
    __tablename__="creative_works"
    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String(32),index=True)
    name=db.Column(db.String(128),index=True)
    tmdb_id = db.Column(db.Integer(),unique=True,index=True)
    same_as = db.Column(db.String(64),unique=True)
    articles = db.relationship('Article',backref='subject',lazy='dynamic')
    image=db.Column(db.Text())
    date_published=db.Column(db.DateTime())
    directed_by = db.relationship('Person',secondary=director_relationship,backref=db.backref('directed',lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return "<{type} \"{name}\">".format(type=self.type,name=self.name)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id':self.id,
            'type':self.type,
            'name':self.name,
            'tmdb_id':self.tmdb_id,
            'same_as':self.same_as,
            'image':self.image,
            'date_published':self.date_published.strftime("%Y-%m-%d"),
            'directed_by': [director.name for director in self.directed_by.all()]
        }

class Person(db.Model):
    __tablename__="people"
    id=db.Column(db.Integer,primary_key=True)
    tmdb_id = db.Column(db.Integer(),unique=True,index=True)
    name = db.Column(db.String(64),index=True)

    def __repr__(self):
        return f'<Person "{self.name}">'


db.event.listen(Article.body, 'set', Article.on_changed_body)
db.event.listen(Article.title,'set', Article.on_changed_title)
db.event.listen(Article.rating,'set', Article.on_changed_rating)
