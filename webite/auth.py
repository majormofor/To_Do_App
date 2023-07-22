# blueprint of our url, render pages, get and post request
from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash  # to flash a message to users
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # remember this user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        user = User.query.filter_by(email=email).first()
        if User:
            flash('Email already exist ', category='error')
        if len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 3:
            flash('Firstname must be greater than 3 characters.', category='error')
        elif len(password) < 8:
            flash('Password must be greater than 7 characters.', category='error')
        elif password != confirmpassword:
            flash('Passwords does not match.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)  # add new user to database
            db.session.commit()  # changes made update
            login_user(new_user, remember=True)  # remember this user
            flash('Account created.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
