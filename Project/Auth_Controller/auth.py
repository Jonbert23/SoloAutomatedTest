from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('tcc.testcode'))
    return render_template('Auth/Login.html', value=current_user.is_authenticated)

    

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('tcc.testcode'))


# @auth.route('/signup')
# def signup():
#     if (current_user.is_authenticated):
#         return redirect(url_for('tcc.testcode'))
#     return render_template('Auth/Register.html')


@auth.route('/signup', methods=['POST','GET'])
@login_required
def signup_post():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists', 'error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), role='admin')
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully register the user', 'success')
         
    return redirect('/')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))