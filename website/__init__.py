# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from testcontainers.postgres import PostgresContainer
# from flask_login import LoginManager
#
# db = SQLAlchemy()
# # DB_NAME = "database.db"
#
# postgres_container = PostgresContainer('postgres:9.5')
# postgres_container.start()
# engine = db.create_engine(postgres_container.get_connection_url())
#
# def create_app():
#     app = Flask(__name__)
#
#     app.config['SECRET_KEY'] = 'afsdadfsasdf'
#
#     print(postgres_container.get_connection_url())
#     app.config['SQLALCHEMY_DATABASE_URI'] = postgres_container.get_connection_url()
#     db.init_app(app)
#
#     from .views import views
#     from .auth import auth
#
#     app.register_blueprint(views, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')
#
#     from .models import Employee, LunchCard
#
#     with app.app_context():
#         db.create_all()
#         print('Database created!')
#
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)
#
#     @login_manager.user_loader
#     def load_user(id):
#         return Employee.query.get(int(id))
#
#     return app
