from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        employee = Employee.query.filter_by(email=email).first()
        if employee:
            if check_password_hash(employee.password, password):
                flash('Login successful!', category='success')
                login_user(employee, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='validation-error')
        else:
            flash('User does not exist!', category='validation-error')

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
        first_name = request.form.get('first-name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        employee = Employee.query.filter_by(email=email).first()

        if employee:
            flash('Email already exists!', category='validation-error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='validation-error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='validation-error')
        elif password != confirm_password:
            flash('Passwords do not match', category='validation-error')
        elif len(password) < 7:
            flash('Password must be greater than 6 characters', category='validation-error')
        else:
            new_employee = Employee(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_employee)
            db.session.commit()

            login_user(new_employee, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)