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

	def test_mostra_ricetta_in_base_a_nome(self):
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		self.client().post('/ricette/', data=ricetta)

		nome = {'NomeRicetta': 'Pasta'}
		res = self.client().post('/mostra/', data=nome)
		self.assertEqual(res.status_code, 200)
		self.assertIn('Pasta', str(res.data))
		self.assertIn('fare pasta', str(res.data))

	def test_creazione_ingrediente(self):
		ingrediente = {'NomeIngrediente': 'Olio'}
		res = self.client().post('/ingrediente/', data=ingrediente)
		self.assertEqual(res.status_code, 201)

	def test_creazione_ingredienti(self):
		ingrediente = {'NomeIngrediente': 'Sugo'}
		res = self.client().post('/ingrediente/', data=ingrediente)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Sugo', str(res.data))

		ingrediente = {'NomeIngrediente': 'Brodo'}
		res = self.client().post('/ingrediente/', data=ingrediente)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Brodo', str(res.data))

	def test_mostra_ingredienti_creati(self):
		self.test_creazione_ingredienti()
		res = self.client().get('/ingrediente/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('Sugo', str(res.data))
		self.assertIn('Brodo', str(res.data))

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()