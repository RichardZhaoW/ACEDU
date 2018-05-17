# -*- coding: UTF-8 -*-
#coding=utf-8
from flask import Flask, render_template, flash, redirect, request, url_for, abort, g
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import current_user, login_required, fresh_login_required
import redis
import pymysql

app = Flask(__name__,static_folder='statics', static_url_path='', template_folder='')
app.secret_key = '1234567'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
SQLHOST = "rm-2zex7u1bczx7a738v.mysql.rds.aliyuncs.com"
users = [{'username':'admin', 'password':'admin'}, {'username':'test', 'password':'test'}]
class User(UserMixin):
    def is_active(self):
        mobile = self.get_id()
        return exist_redis_user(mobile)
    
def query_user(username):
    print "QUERY_USER %s" % username
    if exist_redis_user(username):
        return {'username':username}
    else:
        return None

#def query_user(username):
#    sql = 'select user, password from users where user=%s;'
#    params = [username]
#    bOK, rows = executeSQL(sql, params)
#    print 'rows = %s' % str(rows)
#    if bOK and rows and rows[0]:
#        return {'username':username, 'password':rows[0][1]}
#    else:
#        return None

#def query_user(username):
#    for user in users:
#        if user['username'] == username:
#            return user

@login_manager.user_loader
def load_user(username):
    print "LOAD_USER %s" % username
    if query_user(username):
        curr_user = User()
        curr_user.id = username
        return curr_user
    return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    print "UNAUTH HANDLER"
    return redirect(url_for('login'))

@app.route('/captcha/<mobile>', methods=['GET'])
def captcha(mobile):
    print "CAPTCHA %s" % mobile
    if not validateMobileNumber(mobile):
        return "INVALID PHONE NUMBER"
    if suspend_redis_user(mobile):
        return "REQUEST TOO FREQUENTLY" 
    import random
    code = random.randint(100000, 999999)
    
    send_sms(mobile, code)
    create_redis_user(mobile, code)
    return ''

@app.route('/info', methods=['GET'])
@login_required
def info():
    print "INFO"
    userinfo = getUserInfo()
    if userinfo:
        return render_template('info.html', userinfo=userinfo)
    else:
        print "NO USERINFO!!!"
        return redirect(url_for('register'))

def getDefaultUserInfo():
    userinfo = {}
    userinfo["fullname"] = ""
    userinfo["idcard"] = ""
    userinfo["mobile"] = ""
    userinfo["school"] = ""
    userinfo["email"] = ""
    userinfo["title"] = ""
    userinfo["subject"] = ""
    userinfo["invoice"] = ""
    userinfo["taxno"] = ""
    userinfo["dateArrival"] = ""
    userinfo["dateDeparture"] = ""
    userinfo['male'] = "checked"
    userinfo['female'] = ""
    userinfo['t1'] = 'checked'
    userinfo['t2'] = ''
    userinfo['t3'] = ''
    userinfo['tn'] = ''
    userinfo['act1'] = 'checked'
    userinfo['act2'] = ''
    userinfo['act3'] = ''
    userinfo['lunchYes'] = ''
    userinfo['moslemYes'] = ''
    userinfo['shuttleYes'] = ''    
def getUserInfo():
    userinfo = {}
    if not current_user:
        return userinfo
    sql = selectSQL_info()
    params = [current_user.get_id()]
    bOK, rows = executeSQL(sql, params)
    if bOK and rows:
        row = list(rows[0])
        userinfo['fullname'] = row[0]
        userinfo['gender'] = row[1]
        userinfo['idcard'] = row[2]
        userinfo['mobile'] = row[3]
        userinfo['school'] = row[4]
        userinfo['email'] = row[5]
        userinfo['level'] = row[6]
        userinfo['subject'] = row[7]
        userinfo['invoice'] = row[8]
        userinfo['taxno']  = row[9]
        userinfo['occurence'] = row[10]
        activityType = row[11]
        isLunch = row[12]
        isMoslem = row[13]
        isShuttle = row[16]
        userinfo['activityType'] = index2type(activityType)
        userinfo['isLunch'] = bool2str(isLunch)
        userinfo['isMoslem'] = bool2str(isMoslem)
        userinfo['dateArrival'] = row[14]
        userinfo['dateDeparture'] = row[15]
        userinfo['isShuttle'] = bool2str(isShuttle)
        
        
        userinfo['male'] = ''
        userinfo['female'] = ''
        if userinfo['gender'] == u"男":
            userinfo['male'] = 'selected'
        if userinfo['gender'] == u"女":
            userinfo['female'] = 'selected'
        
        userinfo['t1'] = ''
        userinfo['t2'] = ''
        userinfo['t3'] = ''
        userinfo['tn'] = ''
        if userinfo['occurence'] == 1:
            userinfo['t1'] = 'checked'
        if userinfo['occurence'] == 2:
            userinfo['t2'] = 'checked'
        if userinfo['occurence'] == 3:
            userinfo['t3'] = 'checked'
        if userinfo['occurence'] == 4:
            userinfo['tn'] = 'checked'
        
        userinfo['act1'] = ''
        userinfo['act2'] = ''
        userinfo['act3'] = ''
        if activityType == 1:
            userinfo['act1'] = 'checked'
        if activityType == 2:
            userinfo['act2'] = 'checked'
        if activityType == 3:
            userinfo['act3'] = 'checked'
        
        userinfo['lunchYes'] = ''
        if isLunch == 1:
            userinfo['lunchYes'] = 'checked'
        
        userinfo['moslemYes'] = ''
        if isMoslem == 1:
            userinfo['moslemYes'] = 'checked'
            
        userinfo['shuttleYes'] = ''
        if isShuttle == 1:
            userinfo['shuttleYes'] = 'checked'
    return userinfo

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.get_id():
        redirect(url_for('info'))
        
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        captcha = request.form.get('captcha')
        if validate_redis_user(mobile, captcha):
            confirm_redis_user(mobile)
            print "USER VALIDATED"
            curr_user = User()
            curr_user.id = mobile
            login_user(curr_user, remember=False)
            return redirect(url_for('info'))
        flash('验证码不正确')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    print "LOGOUT"
    logout_user()
    return 'Logged out successfully!'

@app.route("/register", methods=['GET','POST'])
@login_required
def register():
    print "REGISTER"
    if request.method == 'POST':
        form = request.form
        sql = insertStatement(form)
        bOK, _ = executeSQL(sql)
        if bOK:
            return redirect(url_for('info'))
        else:
            return u'报名失败,\n请联系ioe-te@pku.edu.cn'
    userinfo = getUserInfo()
    if not userinfo:
        userinfo = getDefaultUserInfo()
    return render_template('register.html', userinfo=userinfo)

def insertStatement(form):
    isLunch = form.get('isLunch', 0)
    isMoslem = form.get('isMoslem', 0)
    isShuttle = form.get('isShuttle', 0)
    sql = u"INSERT INTO acedu.register" \
          "(idcard, mobile, fullname, email, school, gender, level, subject, invoice, taxno," \
          "occurence, activityType, isLunch, isMoslem, isShuttle, dateArrival, dateDeparture)" \
          "values({idcard}, {mobile}, '{fullname}', '{email}', '{school}', '{gender}', '{level}', '{subject}', '{invoice}', '{taxno}', " \
          "{occurence}, '{activityType}', {isLunch}, {isMoslem}, {isShuttle}, '{dateArrival}', '{dateDeparture}');".format(
        idcard=form['idcard'], mobile=form['mobile'], fullname=form['fullname'], email=form['email'], invoice=form['invoice'],
        school=form['school'], gender=form['gender'], level=form['level'], subject=form['subject'],taxno=form['taxno'],
        occurence=form['occurence'], activityType=form['activityType'], isLunch=isLunch, isMoslem=isMoslem,
         isShuttle=isShuttle, dateArrival=form['dateArrival'], dateDeparture=form['dateDeparture']
    )
    return sql

def selectSQL_info():
    sql = "SELECT fullname, gender, idcard, mobile, school, email, level, subject,"\
          "invoice, taxno, occurence, activityType, isLunch, isMoslem, dateArrival, dateDeparture, isShuttle "\
          "from acedu.register where mobile=%s order by id desc;"
    return sql

def executeSQL(sql, params=None):
    db = None
    bOK, rows = False, []
    try:
        print 'SQL: %s' % sql
        db = pymysql.connect(host=SQLHOST, db='acedu', user='root', passwd='Wlt@2018Up', use_unicode=True, charset='utf8')
        cursor = db.cursor()
        count = cursor.execute(sql, params)
        if count > 0:
            rows = cursor.fetchall()
            rows = list(rows)
        db.commit()
        cursor.close()
        bOK = True
    except Exception, ex:
        bOK = False
        print 'failed to execute: %s' % str(ex)
    finally:
        if db:
            db.close()
    return bOK, rows

def bool2str(boolValue):
    return u'是' if boolValue else u'否'

def index2type(index):
    ret = u'年会+教师工作坊'
    if index == 1:
        ret =  u'年会'
    elif index == 2:
        ret = u'教师工作坊'
    return ret
    
def validateMobileNumber(mobile):
    import re
    pattern = '^(((13[0-9]{1})|(14[0-9]{1})|(17[0-9]{1})|(15[0-3]{1})|(15[4-9]{1})|(18[0-9]{1})|(199))+\d{8})$'
    return bool(re.findall(pattern, mobile))
    
def send_sms(mobile, code):
    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf-8')
    from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.profile import region_provider
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"
    ACCESS_KEY_ID = "LTAIXqQ3Ll4jEwaF"
    ACCESS_KEY_SECRET = "Gc9lYxtzDMpe7DfXhcYKJ6OQoz9DT9"
    template_code = "SMS_134815193"
    sign_name = u"年会报名系统"
    
    acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)
    smsRequest.set_TemplateParam({'code':str(code)})
    smsRequest.set_SignName(sign_name)
    smsRequest.set_PhoneNumbers(str(mobile))
    acs_client.do_action_with_exception(smsRequest)

def create_redis_user(mobile, captcha):
    r = redis.Redis(connection_pool = redis_pool)
    r.set(mobile, captcha, ex=300)
    r.set('suspend%s' % mobile, 1, ex=60)

def suspend_redis_user(mobile):
    r = redis.Redis(connection_pool = redis_pool)
    return bool(r.get('suspend%s' % mobile))
    
def validate_redis_user(mobile, code):
    if not code: return False
    r = redis.Redis(connection_pool = redis_pool)
    captcha = r.get(mobile)
    return captcha == code

def confirm_redis_user(mobile):
    r = redis.Redis(connection_pool = redis_pool)
    r.set('user%s'%mobile, 1, ex=600)
    
def exist_redis_user(mobile):
    r = redis.Redis(connection_pool = redis_pool)
    return bool(r.get('user%s'%mobile))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
