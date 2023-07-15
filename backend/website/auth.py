from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f'Username = {username}')
        
        user = User.query.filter_by(username=username).first()
        if user: 
            if check_password_hash(user.password, str(password)):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
            else:
                flash('Incorrect username/password', category='error')
        else:
            flash('Account does not exist', category='error')
        
        return redirect(url_for('views.homePage'))
        
    return render_template("login.html", user=current_user)


@auth.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user1 = User.query.filter_by(username=username).first()
        user2 = User.query.filter_by(username=email).first()
        if user1:
            flash('account with provided username already exists', category='error')
        elif user2:
            flash('account with provided email already exists',category='error')
        elif(len(str(password1)) < 8):
            flash('password must be greater than 8 characters', category='error')
        elif(password1 != password2):
            flash('passwords do not match', category='error')
        else: 
            new_user = User(username=username, password=generate_password_hash(str(password1), method='scrypt'), email=email, firstname=firstname, lastname=lastname)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.homePage'))
        
    # html that is being run on the page
    return render_template("sign-up.html", user=current_user)

