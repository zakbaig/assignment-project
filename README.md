# Lunch Coupon Service

The Lunch Coupon Service allows users to register an account and login to then be able to add lunch coupons to their account which provide a discount for the office canteen. Users can also modify their profile information as well as the discounts on their existing lunch coupons. Newly created users are given the 'Regular' user role which allows the ability to create new lunch coupons and edit both their user information and existing coupons. The appropriate links can be found in the navigation bar.

There are 3 user roles within this service - 'Regular', 'Admin', and 'Super Admin'. The application comes installed with a Super Admin account and there can be only 1 Super Admin user. Unlike Admin accounts, the Super Admin account cannot be deleted nor can its role be changed. Both Admin and Super Admin users can elevate the role of a Regular user by going to the Admin page and then hitting the 'Edit User' button. This then presents a form where the Role and other user information can be updated. Admin users can delete both user records and lunch coupon records.

Super Admin user credentials - (Email Address = admin@example.com) (Password = nimda321)

All account passwords are stored hashed and not in plain text.

## Technology

This web application has been built using Python's Flask framework. An SQLite database is used during development for fast feedback. The application has been deployed via Heroku and uses a PostgreSQL database in the deployed environment. The web app can be found at this link: https://flask-lunch-coupon-service-2fb8336bc15f.herokuapp.com/

The database uses 2 tables - a User table and a LunchCoupon table. The User table has a one-to-many relationship with the LunchCoupon table. An entity relationship diagram can be found below.

![Screenshot](https://github.com/zakbaig/assignment-project/assets/59240081/caf3663c-31f8-4f45-8225-31943ce38404)

Various Flask dependencies are used to build the application:

- Flask-Login handles user session management
- Flask-SQLAlchemy is used as the ORM (no raw SQL is executed as queries are executed through the ORM)
- Flask-WTF builds the forms in an easy to manage way
- Flask-Migrate handles database migrations
  - Everything within the 'migrations' directory has been automatically generated by Flask-Migrate CLI commands
- Flask-Bootstrap has been used to improve the front-end design

All these dependencies are initialised in one place - the __init__.py file within the 'app' directory.

## Run Locally

To run this application on your machine:
- git clone the repo
- Create a virtual Python environment e.g. `python -m venv venv`
- Install the packages listed in the requirements.txt file - `python -m pip install -r requirements.txt`
- Use Flask-Migrate CLI commands to initialise the database - `flask db init; flask db migrate; flask db upgrade`
- Finally run `flask run`