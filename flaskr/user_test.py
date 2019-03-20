import unittest

from app import db, create_app, apply_views_and_security
from app.models import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        apply_views_and_security(self.app)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

    def test_encode_auth_token(self):
        with self.app.app_context():
            user = User(email='prova@gmail.com', username='prova', password='password')
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        with self.app.app_context():
            user = User(email='prova@gmail.com', username='prova', password='password')
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 'prova@gmail.com')

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()