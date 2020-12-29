import time
from flask import Flask, render_template, request,redirect
import pymysql
app = Flask(__name__)
def connectsql(journal,content,option):
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="19980502", db="stu")
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    rseult = cursor.fetchall()
    return rseult
def getfields(table):
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="19980502", db="stu")
    cursor = conn.cursor()
    sql = "select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name=\'{0}\' and table_schema='stu'".format(table)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    rseult = cursor.fetchall()
    return rseult
def ifClassTwo(user,password):
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="19980502", db="stu")
    cursor = conn.cursor()
    sql = "select * from stu.class where name=\'{0}\' and number=\'{1}\'".format(user,password)
    cursor.execute(sql)
    cursor.close()
    conn.close()
    rseult = cursor.fetchall()
    if(rseult):
        return True
    else:
        return False
@app.route("/login",methods=["get","post"])
def login():
    if(request.method=="GET"):
        return render_template("login.html")
    else:
        user = request.form.get("user")
        password = request.form.get("pwd")
        if(ifClassTwo(user,password)==True):
            return redirect("/")
        return render_template("login.html", error="用户或者密码输入错误")


@app.route('/', methods=['get', 'post'])
def index():
    nowtime = []
    timeobj = time.localtime()
    nowtime.append(str(timeobj.tm_year))
    nowtime.append(str(timeobj.tm_mon))
    nowtime.append(str(timeobj.tm_mday))
    nowtimestr = "-".join(nowtime)
    data = ""
    if request.method == 'POST':
        type = request.form.get("type")
        content = request.form.get('content')
        option = request.form.get('optionsRadios')
        if(type=="journal1"):
            fieldstuple = getfields(type)
            journalFields= []
            degreeFields = None
            for i in fieldstuple:
                for j in i:
                    journalFields.append(j)
            data = connectsql(type, content, option)
            return render_template('index.html', data=data,journalFields=journalFields,degreeFields=degreeFields,nowtimestr=nowtimestr)
        elif(type=="degree"):
            fieldstuple = getfields(type)
            journalFields = None
            degreeFields = []
            for i in fieldstuple:
                for j in i:
                    degreeFields.append(j)
            data= connectsql(type, content, option)
            return render_template('index.html', data=data,journalFields=journalFields,degreeFields=degreeFields, nowtimestr=nowtimestr)
    return render_template('index.html',nowtimestr=nowtimestr, data=data)





if __name__ == '__main__':
    app.run()
