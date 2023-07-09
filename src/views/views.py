from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from src.services import user_service

views = Blueprint('views', __name__)


def exit_with_validation_error(message, template_file):
    flash(message, category='validation-error')
    return render_template(template_file, user=current_user)


def get_sign_up_form(request_form):
    return {
        'email': request_form.get('email'),
        'first_name': request_form.get('first-name'),
        'last_name': request_form.get('last-name'),
        'password': request_form.get('password'),
        'confirm_password': request_form.get('confirm-password')
    }


def validate_sign_up_inputs(request_form):
    form = get_sign_up_form(request_form)
    user = user_service.get_user_by_email(form['email'])
    if user:
        return exit_with_validation_error('Email already exists', 'sign_up.html')
    elif len(form['email']) < 4:
        return exit_with_validation_error('Email must be greater than 3 characters', 'sign_up.html')
    elif len(form['first_name']) < 2:
        return exit_with_validation_error('First name must be greater than 1 character', 'sign_up.html')
    elif len(form['last_name']) < 2:
        return exit_with_validation_error('Last name must be greater than 1 character', 'sign_up.html')
    elif len(form['password']) < 7:
        return exit_with_validation_error('Password must be greater than 6 characters', 'sign_up.html')
    elif form['password'] != form['confirm_password']:
        return exit_with_validation_error('Passwords do not match', 'sign_up.html')
    else:
        new_user = user_service.create_new_user(
            form['email'], form['first_name'], form['last_name'], form['password']
        )
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.home'))


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = user_service.get_user_by_credentials(email, password)
        if user is None:
            return exit_with_validation_error('Incorrect credentials', 'login.html')
        else:
            flash('Login successful', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))


@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return validate_sign_up_inputs(request.form)

    return render_template('sign_up.html', user=current_user)
