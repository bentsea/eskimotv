import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "zEC1yH6twLV5bI7pDP7d"
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '25')
    MAL_USE_TLS = os.environ.get('MAIL_USE_TLS','false').lower() in ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ESKIMOTV_MAIL_SUBJECT_PREFIX = '[EskimoTV]'
    TITLE = "EskimoTV"
    EMAIL = "movieinfo@eskimotv.net"
    DESCRIPTION = "A home for critical and honest reviews that strive for a thoughtful exploration of all forms of art and expression, especially reviews of movies, music, TV, and games!"
    ESKIMOTV_MAIL_SENDER = 'EskimoTV Service Droid <no-reply@eskimotv.net>'
    ESKIMOTV_ADMIN = os.environ.get('ESKIMOTV_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANALYTICS = os.environ.get('ANALYTICS')

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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir,'data.sqlite'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
