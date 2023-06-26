from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first-name')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm-password')

        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='validation-error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='validation-error')
        elif password != confirmPassword:
            flash('Passwords do not match', category='validation-error')
        elif len(password) < 7:
            flash('Password must be greater than 6 characters', category='validation-error')
        else:
            flash('Account created!', category='success')

    return render_template("sign_up.html")