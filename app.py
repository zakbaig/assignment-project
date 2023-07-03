from flask import Flask
from flask_login import LoginManager
from src.database import PostgresClient


def start():
    app = Flask(__name__)
    postgres_client = PostgresClient()
    db = postgres_client.get_sqlalchemy()

    app.config['SECRET_KEY'] = 'afsdadfsasdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_client.get_connection_url()
    db.init_app(app)

    from src.views import views
    from src.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()
        print('Database created!')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from src.database import Employee
        return Employee.query.get(int(id))

    app.run()


if __name__ == '__main__':
    start()
