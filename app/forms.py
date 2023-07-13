from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditUserForm(FlaskForm):
    email_address = StringField('Email Address', validators=[Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    role = StringField('Role')
    submit = SubmitField('Confirm Edit')

    def __init__(self, original_email_address, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_email_address = original_email_address

    def validate_email_address(self, email_address):
        if not email_address.data == self.original_email_address:
            user = User.query.filter_by(email_address=email_address.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')
