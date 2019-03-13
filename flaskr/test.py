from flask import json
from app import create_app, db

import unittest


class DatabaseTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_cl
		
		with self.app.app_context():
			db.create_a

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()