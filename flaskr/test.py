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
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		res = self.client().post('/ricette/', data=ricetta)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Pasta', str(res.data))

		ricetta = {'NomeRicetta': 'Panino', 'Procedimento': 'fare panino'}
		res = self.client().post('/ricette/', data=ricetta)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Panino', str(res.data))

	def test_mostra_ricette_create(self):
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		self.client().post('/ricette/', data=ricetta)
		ricetta = {'NomeRicetta': 'Panino', 'Procedimento': 'fare panino'}
		self.client().post('/ricette/', data=ricetta)

		res = self.client().get('/ricette/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('Pasta', str(res.data))
		self.assertIn('Panino', str(res.data))

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()