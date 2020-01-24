from flask import Flask, render_template
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_assets import Environment, Bundle
from flask_migrate import Migrate
from flask_images import Images
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect

mail=Mail()
moment=Moment()
db=SQLAlchemy()
bootstrap=Bootstrap()
assets=Environment()
migrate = Migrate()
image = Images()
ckeditor = CKEditor()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    image.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)

    assets._named_bundles = {}

    scss = Bundle('css/main.scss',filters="pyscss",output="gen/main.css")
    all_css = Bundle('css/bootstrap.min.css','css/owl.carousel.css','css/owl.theme.css','css/owl.transitions.css','css/social-share-kit.css',scss,filters="cssmin",output="gen/all.css")
    assets.register('all_css',all_css)

    js = Bundle('js/*.js',filters="jsmin",output="gen/all.js")
    assets.register('all_js',js)

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
