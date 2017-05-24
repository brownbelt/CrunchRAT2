# Working authentication code
# Source: https://github.com/maxcountryman/flask-login

import flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from gevent.wsgi import WSGIServer
import os

app = flask.Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
login_manager = LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'admin': {'pw': 'secret'}}

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__ == "__main__":
    # starts Flask listener
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
