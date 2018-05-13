from flask import Flask, render_template, flash, redirect, request
app = Flask(__name__,static_folder='', static_url_path='', template_folder='')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        print email
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)