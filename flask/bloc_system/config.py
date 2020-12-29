class Config():
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19980502@localhost/stu'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True