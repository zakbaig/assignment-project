from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import flask_app, db
from app.forms import LoginForm, RegistrationForm, EditUserForm
from app.models import User, Role


def redirect_to_previous_page_or_index():
    previous_page = request.args.get('next')
    if not previous_page or urlparse(previous_page).netloc != '':
        previous_page = url_for('index')

    return redirect(previous_page)


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
        return redirect_to_previous_page_or_index()

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
    if not current_user.has_role('Admin'):
        return redirect_to_previous_page_or_index()

    users = User.query.all()
    return render_template('admin.html', title='Admin', users=users)


@flask_app.route('/edit_user/<string:user_id>')
@login_required
def edit_user(user_id):
    user = User.query.get(int(user_id))
    if not user == current_user and not current_user.has_role('Admin'):
        return redirect_to_previous_page_or_index()

    form = EditUserForm()
    if request.method == 'GET':
        form.email_address.data = user.email_address
        form.password.data = user.password
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
    elif form.validate_on_submit():
        pass
    return render_template('edit_user.html', title='Edit User', user=user, form=form)
