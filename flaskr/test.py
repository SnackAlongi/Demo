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
		ricetta = { 'NomeRicetta': 'Gallina', 'Procedimento': 'fare arrosto' }
		res = self.client().post('/ricette/', data=ricetta)
		self.assertEqual(res.status_code, 201)

	def test_creazione_ricette(self):
		ricette = [{
			'NomeRicetta': 'Pasta',
			'Procedimento': 'fare pasta'
		},
		{
			'NomeRicetta': 'Panino',
			'Procedimento': 'fare panino'
		}]
		res = self.client().post('/ricette/', data=ricette)
		self.asserEqual(res.status_code, 201)
		self.assertIn('Gallina', str(res.data))
		self.assertIn('Pasta', str(res.data))
		self.assertIn('Panino', str(res.data))


	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()