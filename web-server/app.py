from flask import Flask, request, render_template, session
from forms import LoginForm
from flask_bootstrap import Bootstrap
# from flask_wtf import CSRFProtect
# from flask_login import login_user
import hashlib
from db_server import get_credentials
import os

app = Flask(__name__, static_url_path='/static/')
bootstrap = Bootstrap(app=app)
# csrf = CSRFProtect(app=app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello_world():
    # return 'Hello Stranger! You need to log in.'
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode()
        hash_passw = hashlib.sha256(password).hexdigest()
        if get_credentials(username, hash_passw) == 'Login error':
            return 'Sorry, your credentials are wrong'
        else:
            user, passwd = get_credentials(username, hash_passw)
            print(user, passwd)

            if user and passwd:
                session['username'] = form.username.data
                return 'got it', session
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
