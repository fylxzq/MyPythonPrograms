from flask import redirect,url_for
import pymysql
import re
from . import main
from ..models import User
from ..models import db
def table_exist():
    connect = pymysql.connect(user='root',host='localhost',password='19980502',db='stu',port=3306)
    sql = 'show tables'
    cursor = connect.cursor()
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if('users' in table_list):
        return True
    else:
        return False

@main.route('/',methods=['GET','POST'])
def index():
    db.create_all()
    return redirect(url_for('auth.login'))