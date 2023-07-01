from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from testcontainers.postgres import PostgresContainer

app = Flask(__name__)
db = SQLAlchemy()
# DB_NAME = "database.db"

postgres_container = PostgresContainer('postgres:9.5')
postgres_container.start()
engine = db.create_engine(postgres_container.get_connection_url())


@app.route('/')
@login_required
def index():
    return render_template('home.html', user=current_user)


def start():
    app.config['SECRET_KEY'] = 'afsdadfsasdf'



if __name__ == '__main__':
    app.run()
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_container.get_connection_url()
    db.init_app(app)