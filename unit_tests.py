import os
import unittest
from app import flask_app, db
from app.models import User, LunchCoupon

os.environ['DATABASE_URL'] = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = flask_app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(email_address='test@example.com')
        user.set_password('test')
        self.assertFalse(user.password == 'test')
        self.assertFalse(user.check_password('Test'))
        self.assertTrue(user.check_password('test'))

if __name__ == '__main__':
    unittest.main(verbosity=2)