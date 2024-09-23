

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/fierce_app'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JWT_SECRET_KEY = 'HS256'
   
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'anitahnansa@gmail.com'
    MAIL_PASSWORD = 'Nansalre@21'
    MAIL_DEFAULT_SENDER = 'anitahnansa@gmail.com'
