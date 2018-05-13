# -*- coding: UTF-8 -*-
#coding=utf-8
from flask import Flask, render_template, flash, redirect, request
import pymysql
app = Flask(__name__,static_folder='', static_url_path='', template_folder='')
SQLHOST = "rm-2zex7u1bczx7a738v.mysql.rds.aliyuncs.com"

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        form = request.form
        sql = insertStatement(form)
        print sql
        executeSQL(sql)
        return u'注册成功'
    return render_template('index.html')

def insertStatement(form):
    sql = u"INSERT INTO acedu.register" \
          "(idcard, mobile, fullname, email, school, gender, level, subject, " \
          "occurence, activityType, isLunch, isMoslem, isShuttle, dateArrival, dateDeparture)" \
          "values({idcard}, {mobile}, '{fullname}', '{email}', '{school}', '{gender}', '{level}', '{subject}', " \
          "{occurence}, '{activityType}', {isLunch}, {isMoslem}, {isShuttle}, '{dateArrival}', '{dateDeparture}');commit;".format(
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
        db = pymysql.connect(host=SQLHOST, db='acedu', user='root', passwd='Wlt@2018Up')
        cursor = db.cursor()
        count = cursor.execute(sql)
        if count > 0:
            rows = cursor.fetchall()
            rows = list(rows)
        cursor.close()
    except Exception, ex:
        bOK = False
        print ex
    finally:
        if db:
            db.close()
    return bOK, rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)