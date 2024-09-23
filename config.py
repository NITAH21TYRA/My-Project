

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/fierce_app'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JWT_SECRET_KEY = '12345'
    JWT_TOKEN_LOCATION = ['headers'] 
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'moriahnakazibwe@gmail.com'
    MAIL_PASSWORD = 'Moriah@001'
    MAIL_DEFAULT_SENDER = 'your-email@exaz zmple.com'
