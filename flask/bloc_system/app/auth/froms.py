from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,IntegerField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from ..models import User
from wtforms import ValidationError
class LoginForm(FlaskForm):
    stunum = IntegerField("学号",validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember_me = BooleanField('密码',validators=[DataRequired()])
    submit = SubmitField('登陆')

class SearchForm(FlaskForm):
    stunum = IntegerField("请输入要查询的学号")
    submit = SubmitField("查询")

class ResistrationForm(FlaskForm):
    stunum = IntegerField("学号",validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or underscores')])
    gender = SelectField("性别",choices=[("male","男"),("female","女")],validators=[DataRequired()])
    buildingnum = IntegerField("楼号",validators=[DataRequired()])
    domitorynum = IntegerField("寝室号",validators=[DataRequired()])
    password = PasswordField("密码",validators=[DataRequired(),EqualTo("password2",message="password must match")])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_eamil(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alrerady register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


