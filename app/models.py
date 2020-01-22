from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
import hashlib

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
        return '<Role {}>'.format(self.name)

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


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    draft = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edit = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    published = db.Column(db.DateTime, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Director(db.Model):
    __tablename__="directs"
    director_id=db.Column(db.Integer,db.ForeignKey('people.id'),primary_key=True)
    work_id=db.Column(db.Integer,db.ForeignKey('creative_works.id'),primary_key=True)

class CreativeWork(db.Model):
    __tablename__="creative_works"
    id=db.Column(db.Integer,primary_key=True)
    #type=db.Column(db.String(32),index=True)
    #name=db.Column(db.String(128),index=True)
    #tmdb_id = db.Column(db.Text(),unique=True,index=True)
    directed_by = db.relationship('Director',
                               foreign_keys=[Director.work_id],
                               backref=db.backref('directed_by', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    #image=db.Column(db.Text())
    #ublished=db.Column(db.DateTime())

class Person(db.Model):
    __tablename__="people"
    id=db.Column(db.Integer,primary_key=True)
    #tmdb_id = db.Column(db.Integer,index=True)
    # #name = db.Column(db.Text(),index=True)
    directed = db.relationship('Director',
                               foreign_keys=[Director.director_id],
                               backref=db.backref('directed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')