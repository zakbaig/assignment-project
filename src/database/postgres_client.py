from flask_sqlalchemy import SQLAlchemy
from testcontainers.postgres import PostgresContainer
from src.helpers import Singleton


class PostgresClient(Singleton):
    def init(self):
        self._sqlalchemy = SQLAlchemy()
        self._postgres_container = PostgresContainer()
        self._postgres_container.start()
        self._connection_url = self._postgres_container.get_connection_url()
        self._sqlengine = self._sqlalchemy.create_engine(self._connection_url)

    def get_sqlalchemy(self):
        return self._sqlalchemy

    def get_postgres_container(self):
        return self._postgres_container

    def get_connection_url(self):
        return self._connection_url

    def get_sqlengine(self):
        return self._sqlengine
