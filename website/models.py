from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class LunchCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(1000))
    # date = db.Column(db.DateTime(timezone=True, default=func.now()))
    date = db.Column(db.DateTime(timezone=True))
    card_balance = db.Column(db.Integer)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    lunch_cards = db.relationship('LunchCard')
