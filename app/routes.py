from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import flask_app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Role


@flask_app.before_request
def before_request():
    admin_email_address = flask_app.config.get('ADMIN_EMAIL_ADDRESS')
    if not User.query.filter(User.email_address == admin_email_address).first():
        user = User(email_address=admin_email_address)
        user.set_password(flask_app.config.get('ADMIN_PASSWORD'))
        user.roles.append(Role(name='Admin'))
        db.session.add(user)
        db.session.commit()


@flask_app.route('/')
@flask_app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials', 'validation-error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@flask_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email_address=form.email_address.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@flask_app.route('/admin')
@login_required
def admin():
    for role in current_user.roles:
        print(role.name)
        if role.name == 'Admin':
            return render_template('admin.html')

    return redirect(url_for('login'))
