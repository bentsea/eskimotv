import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "zEC1yH6twLV5bI7pDP7d"
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '25')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','false').lower() in ['true','on','1']
    MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL','false').lower() in ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ESKIMOTV_MAIL_SUBJECT_PREFIX = '[EskimoTV]'
    TITLE = "EskimoTV"
    EMAIL = "movieinfo@eskimotv.net"
    DESCRIPTION = "A home for critical and honest reviews that strive for a thoughtful exploration of all forms of art and expression, especially reviews of movies, music, TV, and games!"
    ESKIMOTV_MAIL_SENDER = 'EskimoTV Service Droid <no-reply@eskimotv.net>'
    ESKIMOTV_ADMIN = os.environ.get('ESKIMOTV_ADMIN','brokenmind@gmail.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANALYTICS = os.environ.get('ANALYTICS')
    ESKIMOTV_ARTICLES_PER_PAGE = 9
    CKEDITOR_FILE_UPLOADER = 'admin.upload_images'
    CKEDITOR_FILE_BROWSER = 'flaskfilemanager.index'
    FLASKFILEMANAGER_FILE_PATH = os.path.join(basedir,'app/static/uploads/')
    TMDB_API_KEY=os.environ.get('TMDB_API_KEY')
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_EXTRA_PLUGINS = ["youtube","wordcount","notification"]
    IMAGES_CACHE=os.path.join(basedir,"tmp/flask-images")
    primary_color = "#6699cc"
    secondary_color1 = "#003366"
    secondary_color2 = "#336699"
    light_color1 = "#D6EAF8"
    FBAPPID = "969503389844347"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir,'data-dev.sqlite'))
    ASSETS_DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir,'data-test.sqlite'))

class ProductionConfig(Config):
    SERVER_NAME="www.eskimotv.net"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir,'data.sqlite'))
    #ASSETS_DEBUG = True
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.ESKIMOTV_MAIL_SENDER,
            toaddrs=[cls.ESKIMOTV_ADMIN],
            subject=cls.ESKIMOTV_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
