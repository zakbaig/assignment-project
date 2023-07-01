from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from testcontainers.postgres import PostgresContainer

app = Flask(__name__)

postgres_container = PostgresContainer('postgres:9.5')
postgres_container.start()

db = SQLAlchemy()
engine = db.create_engine(postgres_container.get_connection_url())


@app.route('/')
@login_required
def index():
    return render_template('home.html', user=current_user)


def start():
    # postgres_container = PostgresContainer('postgres:9.5')
    # postgres_container.start()
    print(postgres_container.get_connection_url())

    # db = SQLAlchemy()
    # engine = db.create_engine(postgres_container.get_connection_url())

    app.config['SECRET_KEY'] = 'afsdadfsasdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_container.get_connection_url()
    db.init_app(app)

    # from website.auth import auth
    # app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()
        print('Database created!')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from website.models import Employee
        return Employee.query.get(int(id))

    app.run()


if __name__ == '__main__':
    start()
