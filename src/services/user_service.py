from src.database import PostgresClient, User
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None
    else:
        return user


def get_user_by_credentials(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None
    elif not check_password_hash(user.password, password):
        return None
    else:
        return user


def create_new_user(email, first_name, last_name, password):
    postgres_client = PostgresClient()
    new_user = User(email=email, first_name=first_name,
                        last_name=last_name, password=generate_password_hash(password, method='sha256'))
    db = postgres_client.get_sqlalchemy()
    db.session.add(new_user)
    db.session.commit()
    return new_user
