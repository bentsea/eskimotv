from flask import Flask, render_template, current_app,session
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_assets import Environment, Bundle
from flask_migrate import Migrate
from flask_images import Images
from flask_login import LoginManager,current_user
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
import flaskfilemanager

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


    # with app.app_context():
    #     #Define access control for flaskfilemanager.
    #     def file_access_permission():
    #         """
    #         :return: True if the user is allowed to access the filemanager, otherwise False
    #         """
    #         return session.get('user_id',False)
    #
    #     #Restrict flaskfilemanager access ut user directory.
    #     app.config['FLASKFILEMANAGER_FILE_PATH'] = "{}{}/".format(app.config['FLASKFILEMANAGER_FILE_PATH'],session.get('user_id'))

    #Initialize dependencies.
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

    def can_edit_files():
        from app.models import Permission
        return current_user.can(Permission.WRITE)

    assets._named_bundles = {}

    scss = Bundle('css/main.scss',filters="pyscss",output="gen/main.css")
    all_css = Bundle('css/bootstrap.min.css','css/owl.carousel.css','css/owl.theme.css','css/owl.transitions.css','css/social-share-kit.css',scss,filters="cssmin",output="gen/all.css")
    assets.register('all_css',all_css)

    js = Bundle('js/*.js',filters="jsmin",output="gen/all.js")
    assets.register('all_js',js)

    with app.app_context():
        # attach routes and custom error pages here
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .api import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')

        #import the access control after the db has been initialized.
        flaskfilemanager.init(app,access_control_function=can_edit_files)

        return app
