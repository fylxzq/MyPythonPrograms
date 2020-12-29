from flask import render_template,redirect,request,url_for,flash
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from .froms import LoginForm,ResistrationForm,SearchForm
from .. import db

@auth.route('/user/<stunum>',methods=['POST','GET'])
def user(stunum):
    user = User.query.filter_by(stunum=stunum).first()
    name = user.username
    gender = user.gender
    buildingnum = user.buildingnum
    domitorynum = user.domitorynum
    searchform = SearchForm()
    rst = None
    if searchform.validate_on_submit():
        rst  = User.query.filter_by(stunum=searchform.stunum.data).all()
        return render_template('auth/user.html',name=name,stunum=stunum,gender=gender,buildingnum=buildingnum,domitorynum=domitorynum,form=searchform,rst=rst)
    return render_template('auth/user.html',name=name,stunum=stunum,gender=gender,buildingnum=buildingnum,domitorynum=domitorynum,form=searchform)


@auth.route('/revise')
def revise():
    return  redirect(url_for("auth.register"))

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(stunum=form.stunum.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return  redirect(url_for('auth.user',stunum=user.stunum) or request.arg.get('next'))
        flash('Invaild username or password')
    return render_template('auth/login.html',form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = ResistrationForm()
    if form.validate_on_submit():
        user = User(stunum=form.stunum.data,username=form.username.data,gender=form.gender.data,buildingnum=form.buildingnum.data,domitorynum=form.domitorynum.data,password=form.password.data)
        db.session.add(user)
        flash('you can login now')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)



