# -*- coding: UTF-8 -*-
#coding=utf-8
from flask import Flask, render_template, flash, redirect, request, url_for, abort
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user
from flask.ext.login import current_user, login_required, fresh_login_required
import pymysql

app = Flask(__name__,static_folder='', static_url_path='', template_folder='')
app.secret_key = '1234567'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"

SQLHOST = "rm-2zex7u1bczx7a738v.mysql.rds.aliyuncs.com"
users = [{'username':'admin', 'password':'admin'}, {'username':'test', 'password':'test'}]
class User(UserMixin):
    pass

def query_user(username):
    for user in users:
        if user['username'] == username:
            return user

@login_manager.user_loader
def load_user(username):
    if query_user(username):
        curr_user = User()
        curr_user.id = username
        return curr_user
    return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None and request.form['password'] == user['password']:
            curr_user = User()
            curr_user.id = username

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user, remember=True)

            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            next = request.args.get('next')
            return redirect(next or url_for('index'))

        flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

@app.route("/register", methods=['GET','POST'])
@login_required
def register():
    if request.method == 'POST':
        form = request.form
        sql = insertStatement(form)
        print sql
        bOK = executeSQL(sql)
        if bOK:
            return u'报名成功'#outputInfo(form)
        else:
            return u'报名失败,\n请联系ioe-te@pku.edu.cn'
    return render_template('index.html')

def outputInfo(form):
    outputString = u'姓名:\t{fullname}\n性别:\t{gender}身份证号:\t{idcard}\n手机号:\t{mobile}\n邮箱:\t{email}\n' \
                   u'院校:\t{school}\n职务:\t{level}\n学科:\t{subject}\n' \
                   u'抵达日期:\t{dateArrival}\n离会日期:\t{dateDeparture}\n'.format(fullname=form['fullname'],
                                                                            gender=form['gender'],
                                                                            idcard=form['idcard'],
                                                                            mobile=form['mobile'],
                                                                            email=form['email'],
                                                                            school=form['school'],
                                                                            level=form['level'],
                                                                            subject=form['subject'],
                                                                            dateArrival=form['dateArrival'],
                                                                            dateDeparture=form['dateDeparture'])
    return outputString

def insertStatement(form):
    sql = u"INSERT INTO acedu.register" \
          "(idcard, mobile, fullname, email, school, gender, level, subject, " \
          "occurence, activityType, isLunch, isMoslem, isShuttle, dateArrival, dateDeparture)" \
          "values({idcard}, {mobile}, '{fullname}', '{email}', '{school}', '{gender}', '{level}', '{subject}', " \
          "{occurence}, '{activityType}', {isLunch}, {isMoslem}, {isShuttle}, '{dateArrival}', '{dateDeparture}');".format(
        idcard=form['idcard'], mobile=form['mobile'], fullname=form['fullname'], email=form['email'],
        school=form['school'], gender=form['gender'], level=form['level'], subject=form['subject'],
        occurence=form['occurence'], activityType=form['activityType'], isLunch=form['isLunch'], isMoslem=form['isMoslem'],
         isShuttle=form['isShuttle'], dateArrival=form['dateArrival'], dateDeparture=form['dateDeparture']
    )
    return sql

def executeSQL(sql):
    db = None
    bOK, rows = True, []
    try:
        db = pymysql.connect(host=SQLHOST, db='acedu', user='root', passwd='Wlt@2018Up', use_unicode=True, charset='utf8')
        cursor = db.cursor()
        count = cursor.execute(sql)
        if count > 0:
            rows = cursor.fetchall()
            rows = list(rows)
        db.commit()
        cursor.close()
    except Exception, ex:
        bOK = False
        print ex
    finally:
        if db:
            db.close()
    return bOK, rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)