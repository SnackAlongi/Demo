import unittest
from flask import jsonify, json
from app import db, create_app, create_security, create_views
from app.models import User


class TestAuthBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        create_views(self.app)
        create_security(self.app)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()

    def test_registration(self):
        with self.client:
            user = jsonify({'email':'prova@gmail.com', 'password':'123456'})

            response = self.client.post(
                '/auth/register',
                data=user,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()



if __name__ == '__main__':
    unittest.main()