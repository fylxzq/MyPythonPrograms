from flask_login import UserMixin,login_required
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_mangeer
#创建一张用户表
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    stunum = db.Column(db.Integer,unique=True,index=True)
    gender = db.Column(db.String(64))
    username = db.Column(db.String(64))
    buildingnum = db.Column(db.Integer)
    domitorynum = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(permissions=0xff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()


@login_mangeer.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class Role(db.Model):
#     __tablename__  = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ATRICLES,True),
#             'Moderator':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ATRICLES,Permission.MODERATE_COMMENTS,False),
#             'Administrator': (0xff, False)
#         }
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.permissions = roles[r][0]
#             role.default = roles[r][1]
#             db.session.add(role)
#         db.session.commit()
#
#
# class Permission:
#     FOLLOW = 1
#     COMMENT = 2
#     WRITE_ATRICLES = 4
#     MODERATE_COMMENTS = 8
#     ADMINISTER = 16
