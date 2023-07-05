from src.database import PostgresClient, Employee
from werkzeug.security import generate_password_hash, check_password_hash


def get_employee_by_email(email):
    postgres_client = PostgresClient()
    with postgres_client.get_sqlengine().begin():
        employee = Employee.query.filter_by(email=email).first()
        if employee is None:
            return None
        else:
            return employee


def get_employee_by_credentials(email, password):
    postgres_client = PostgresClient()
    with postgres_client.get_sqlengine().begin():
        employee = Employee.query.filter_by(email=email).first()
        if employee is None:
            return None
        elif not check_password_hash(employee.password, password):
            return None
        else:
            return employee


def create_new_employee(email, first_name, last_name, password):
    postgres_client = PostgresClient()
    new_employee = Employee(email=email, first_name=first_name,
                            last_name=last_name, password=generate_password_hash(password, method='sha256'))
    db = postgres_client.get_sqlalchemy()
    db.session.add(new_employee)
    db.session.commit()
    return new_employee
