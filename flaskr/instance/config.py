import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "develop_key"
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///develop.db'
    SESSION_TYPE = 'sqlalchemy'
    SECURITY_PASSWORD_SALT = b'nA\x06O\xaf\x04\xb8\xab\x80\xf24\xc53\xcf\xe1\x1a\xe4N\x1c\xfd\xee5\x806'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fixture.sql'
    DEBUG = True
    SESSION_TYPE = 'sqlalchemy'

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}