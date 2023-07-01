from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, engine
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


def validation_error_exit(message, template_file):
    flash(message, category='validation-error')
    return render_template(template_file, user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with engine.begin():
            email = request.form.get('email')
            employee = Employee.query.filter_by(email=email).first()
            if employee is None:
                return validation_error_exit('User does not exist', 'login.html')

            password = request.form.get('password')
            if not check_password_hash(employee.password, password):
                return validation_error_exit('Incorrect password', 'login.html')
            else:
                flash('Login successful', category='success')
                login_user(employee, remember=True)
                return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        with engine.begin():
            employee = Employee.query.filter_by(email=email).first()
            if employee:
                print(f'Exit from sign-up, this employee already exists - ${employee}')
                return validation_error_exit('Email already exists', 'sign_up.html')

        if len(email) < 4:
            return validation_error_exit('Email must be greater than 3 characters', 'sign_up.html')

        first_name = request.form.get('first-name')
        if len(first_name) < 2:
            return validation_error_exit('First name must be greater than 1 character', 'sign_up.html')

        password = request.form.get('password')
        if len(password) < 7:
            return validation_error_exit('Password must be greater than 6 characters', 'sign_up.html')

        confirm_password = request.form.get('confirm-password')
        if password != confirm_password:
            return validation_error_exit('Passwords do not match', 'sign_up.html')

        new_employee = Employee(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_employee)
        db.session.commit()

        login_user(new_employee, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
