from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import flask_app, db
from app.forms import LoginForm, RegistrationForm, EditUserForm, AddCouponForm, EditCouponForm
from app.models import User, LunchCoupon


def redirect_to_previous_page_or_index():
    previous_page = request.args.get('next')
    if not previous_page or urlparse(previous_page).netloc != '':
        previous_page = url_for('index')

    return redirect(previous_page)


def current_user_is_admin_or_super_admin():
    return current_user.has_role('Admin') or current_user.has_role('Super Admin')


@flask_app.before_request
def before_request():
    admin_email_address = flask_app.config.get('ADMIN_EMAIL_ADDRESS')
    if not User.query.filter(User.email_address == admin_email_address).first():
        user = User(email_address=admin_email_address, role='Super Admin',
                    first_name=flask_app.config.get('ADMIN_FIRST_NAME'),
                    last_name=flask_app.config.get('ADMIN_LAST_NAME'))
        user.set_password(flask_app.config.get('ADMIN_PASSWORD'))
        db.session.add(user)
        db.session.commit()


@flask_app.route('/')
@flask_app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    del form.role

    if form.validate_on_submit():
        user = User(email_address=form.email_address.data,
                    role='Regular',
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


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

        login_user(user)
        return redirect_to_previous_page_or_index()

    return render_template('login.html', title='Login', form=form)


@flask_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@flask_app.route('/admin')
@login_required
def admin():
    if not current_user_is_admin_or_super_admin():
        return redirect_to_previous_page_or_index()

    users = User.query.all()
    return render_template('admin.html', title='Admin', users=users)


@flask_app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user_is_admin_or_super_admin():
        return redirect_to_previous_page_or_index()

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email_address=form.email_address.data,
                    role=form.role.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created.')
        return redirect(url_for('admin'))

    return render_template('create_user.html', title='Create User', form=form)


@flask_app.route('/edit_user/<string:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(int(user_id))
    if not user == current_user and not current_user_is_admin_or_super_admin():
        return redirect_to_previous_page_or_index()

    if not current_user.has_role('Super Admin') and user.has_role('Super Admin'):
        return redirect_to_previous_page_or_index()

    form = EditUserForm(user.email_address)
    if (current_user.has_role('Super Admin') and user.has_role('Super Admin')) or (current_user.has_role('Regular')):
        del form.role

    if request.method == 'GET':
        form.email_address.data = user.email_address
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        if form.role is not None:
            form.role.data = user.role
    elif form.validate_on_submit():
        user.email_address = form.email_address.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        if form.role is not None:
            user.role = form.role.data

        db.session.commit()
        flash('Your changes have been saved.')

    return render_template('edit_user.html', title='Edit User', user=user, form=form)


@flask_app.route('/delete_user/<string:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get(int(user_id))
    if not current_user_is_admin_or_super_admin() or current_user == user:
        return redirect_to_previous_page_or_index()

    if user.has_role('Super Admin'):
        return redirect_to_previous_page_or_index()

    db.session.delete(user)
    db.session.commit()
    flash('User deleted.')
    return redirect(url_for('admin'))


@flask_app.route('/view_coupons/<string:user_id>', methods=['GET', 'POST'])
@login_required
def view_coupons(user_id):
    user = User.query.get(int(user_id))
    return render_template('view_coupons.html', title='View Coupon', user=user)


@flask_app.route('/add_coupon/<string:user_id>', methods=['GET', 'POST'])
@login_required
def add_coupon(user_id):
    user = User.query.get(int(user_id))
    form = AddCouponForm()
    if form.validate_on_submit():
        lunch_coupon = LunchCoupon(discount=form.discount.data)
        user.lunch_coupons.append(lunch_coupon)
        db.session.commit()
        flash('Coupon added.')
        return redirect(url_for('view_coupons', user_id=user_id))

    return render_template('add_coupon.html', title='Add Coupon', form=form, user=user)


@flask_app.route('/edit_coupon/<string:coupon_id>', methods=['GET', 'POST'])
@login_required
def edit_coupon(coupon_id):
    lunch_coupon = LunchCoupon.query.get(int(coupon_id))
    user = User.query.get(int(lunch_coupon.user_id))
    form = EditCouponForm()
    if request.method == 'GET':
        form.discount.data = lunch_coupon.discount
    elif form.validate_on_submit():
        lunch_coupon.discount = form.discount.data
        db.session.commit()
        flash('Coupon edited.')
        return redirect(url_for('view_coupons', user_id=user.id))

    return render_template('edit_coupon.html', title='Edit Coupon', form=form, user=user)


@flask_app.route('/delete_coupon/<string:coupon_id>', methods=['GET', 'POST'])
@login_required
def delete_coupon(coupon_id):
    lunch_coupon = LunchCoupon.query.get(int(coupon_id))
    user = User.query.get(int(lunch_coupon.user_id))
    db.session.delete(lunch_coupon)
    db.session.commit()
    flash('Coupon deleted.')
    return redirect(url_for('view_coupons', user_id=user.id))
