from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(150), index=True, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    lunch_coupons = db.relationship('LunchCoupon')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def has_role(self, role):
        return role == self.role


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class LunchCoupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
