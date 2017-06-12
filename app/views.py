from flask import render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from app import app
from .models import User
#import server

# AUTHENTICATION DEBUGGING!
# Source: https://github.com/maxcountryman/flask-login

login_manager = LoginManager()
login_manager.init_app(app)


users = {'admin': {'pw': 'secret'}}

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
    print(app.server_password)

    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('home'))

    return 'Bad login'


# CODE ABOVE NEEDS CLEANED UP


@app.route('/home', methods=['GET'])
@login_required
def home():
    '''
        DESCRIPTION:
            The user is brought here post-authentication
    '''
    return render_template('home.html'), 200


@app.route('/logout', methods=['GET'])
def logout():
    '''
        DESCRIPTION:
            Logs out the current user and redirects back
            to the login page
    '''
    logout_user()
    return redirect(url_for('login'))
