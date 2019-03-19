import unittest

from app import db, create_app, apply_views_and_security
from app.models import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.userdata_store = apply_views_and_security(self.app)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

    def test_encode_auth_token(self):
        with self.app.app_context():
            user = self.userdata_store.create_user(email="prova@gamil.com", password='password')
            db.session.commit()
            auth_token = User.encode_auth_token(user.email)
        self.assertTrue(isinstance(auth_token, bytes))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()