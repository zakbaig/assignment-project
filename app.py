import secrets
from flask import Flask
from flask_login import LoginManager
from flask_security import SQLAlchemySessionUserDatastore, Security
from src.database import PostgresClient, User, Role
from src.views import views


def start():
    app = Flask(__name__)
    postgres_client = PostgresClient()
    db = postgres_client.get_sqlalchemy()

    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_client.get_connection_url()
    app.register_blueprint(views, url_prefix='/')

    db.init_app(app)
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()
        print('Database created!')

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.run()


if __name__ == '__main__':
    start()
