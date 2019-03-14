from flask import json
from app import create_app, db

import unittest


class DatabaseTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		
		with self.app.app_context():
			db.create_all()

	def test_creazione_ricetta(self):
		ricetta = { 'NomeRicetta' : 'Gallina', 'Procedimento' : 'fare arrosto' }
		res = self.client().post('/ricette/', data=ricetta)
		self.assertEqual(res.status_code, 201)

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()