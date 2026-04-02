class config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:3417@127.0.0.1/jassencebd'
    SQLALCHEMY_TRACK_MODIFCATIONS=False
    # No usar root

    
