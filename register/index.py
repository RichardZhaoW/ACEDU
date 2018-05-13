from flask import Flask, render_template, flash, redirect, request
app = Flask(__name__,static_folder='', static_url_path='', template_folder='')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        print getSQL(form)
        return '注册成功'
    return render_template('index.html')

def getSQL(form):
    sql = "INSERT INTO acedu.register" \
          "(idcard, mobile, fullname, email, school, gender, level, subject, " \
          "occurence, activityType, isLunch, isMoslem, isShuttle, dateArrival, dateDeparture)" \ 
          "values({idcard}, {mobile}, '{fullname}', '{email}', '{school}', '{gender}', '{level}', '{subject}', " \
          "{occurence}, {activityType}, {isLunch}, {isMoslem}, {isShuttle}, '{dateArrival}', '{dateDeparture}');".format(
        idcard=form['idcard'], mobile=form['mobile'], fullname=form['fullname'], email=form['email'],
        school=form['school'], gender=form['gender'], subject=form['subject'],
        occurence=form['occurence'], activityType=form['activityType'], isLunch=form['isLunch'], isMoslem=form['isMoslem'],
         isShuttle=form['isShuttle'], dateArrival=form['dateArrival'], dateDeparture=form['dateDeparture']
    )
    return sql

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)