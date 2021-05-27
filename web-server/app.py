from flask import Flask, request, render_template
from forms import LoginForm
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
# import hashlib
import os

app = Flask(__name__)
bootstrap = Bootstrap(app=app)
csrf = CSRFProtect(app=app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello_world():
    return 'Hello Stranger! You need to log in.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode()
        print(username, password)
        # hash_passw = hashlib.sha256(password)
        if username and password:
            print('Hello,', username)
            return 'yes'
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
