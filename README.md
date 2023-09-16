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
- Git clone the repo
- Create a virtual Python environment e.g. `python -m venv venv`
- Activate the virtual environment e.g. `source venv/bin/activate`
- Install the packages listed in the requirements.txt file - `python -m pip install -r requirements.txt`
- Use Flask-Migrate CLI commands to initialise the database - `flask db init; flask db migrate; flask db upgrade`
- Run the following in the command line `flask run`
- Navigate to localhost in your browser

## Docker

You can also run this application through Docker (uses an in-memory DB).

- Git clone the repo
- Run `docker build -t lunch-coupon-service .`
- Run `docker run -p 80:5000 --env-file=.dockerenv lunch-coupon-service`
- Navigate to localhost in your browser

Docker Compose is also available. Running through Docker Compose simulates a running environment closer to that of the one in production as it creates and uses a separate Postgres container instead of an in-memory DB. This means you can stop and restart the lunch-coupon container and still be able to access data created from before the service was restarted.

- Git clone the repo
- Run `docker-compose up -d`
- Navigate to localhost:5000 in your browser

Instead of cloning the repo and building the Docker image on your machine, you can instead pull the image from the GitLab repo's Container Registry. The CI/CD pipeline automatically builds the image and pushes it to GitLab via the job `docker-image-build-and-push`.

- Login to GitLab's Registry `docker login registry.gitlab.com` (you will need to generate an access token)
- Pull the image `docker pull registry.gitlab.com/zakaria.baig/assignment-project:main`
- Use the image to run the container whilst supplying your own Admin ENV vars `docker run -p 80:5000 --env ADMIN_EMAIL_ADDRESS=[placeholder] --env ADMIN_PASSWORD=[placeholder] --env ADMIN_FIRST_NAME=[placeholder] --env ADMIN_LAST_NAME=[placeholder] registry.gitlab.com/zakaria.baig/assignment-project:main`
- Navigate to localhost in your browser

## Tests

With the Python environment setup correctly (see 'Run Locally' section), unit tests can be run via the following command - `python -m pytest unit_tests.py`