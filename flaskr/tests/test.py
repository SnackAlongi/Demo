from app import create_app, db

import unittest


class jsonbaseTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		
		with self.app.app_context():
			db.create_all()

	def test_creazione_ricetta(self):
		ricetta = {'NomeRicetta': 'Gallina', 'Procedimento': 'fare arrosto'}
		res = self.client().post('/api/ricetta/', json=ricetta)
		self.assertEqual(res.status_code, 201)

	def test_creazione_ricette(self):
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		res = self.client().post('/api/ricetta/', json=ricetta)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Pasta', str(res.json))

		ricetta = {'NomeRicetta': 'Panino', 'Procedimento': 'fare panino'}
		res = self.client().post('/api/ricetta/', json=ricetta)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Panino', str(res.json))

	def test_mostra_ricette_create(self):
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		self.client().post('/api/ricetta/', json=ricetta)
		ricetta = {'NomeRicetta': 'Panino', 'Procedimento': 'fare panino'}
		self.client().post('/api/ricetta/', json=ricetta)

		res = self.client().get('/api/ricetta/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('Pasta', str(res.json))
		self.assertIn('Panino', str(res.json))

	def test_mostra_ricetta_in_base_a_nome(self):
		ricetta = {'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta'}
		self.client().post('/api/ricetta/', json=ricetta)

		nome = {'NomeRicetta': 'Pasta'}
		res = self.client().post('/api/mostra/', json=nome)
		self.assertEqual(res.status_code, 200)
		self.assertIn('Pasta', str(res.json))
		self.assertIn('fare pasta', str(res.json))

	def test_creazione_ingrediente(self):
		ingrediente = {'NomeIngrediente': 'Olio'}
		res = self.client().post('/api/ingrediente/', json=ingrediente)
		self.assertEqual(res.status_code, 201)

	def test_creazione_ingredienti(self):
		ingrediente = {'NomeIngrediente': 'Sugo'}
		res = self.client().post('/api/ingrediente/', json=ingrediente)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Sugo', str(res.json))

		ingrediente = {'NomeIngrediente': 'Brodo'}
		res = self.client().post('/api/ingrediente/', json=ingrediente)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Brodo', str(res.json))

	def test_mostra_ingredienti_creati(self):
		self.test_creazione_ingredienti()
		res = self.client().get('/api/ingrediente/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('Sugo', str(res.json))
		self.assertIn('Brodo', str(res.json))

	def test_aggiungi_ingredienti_e_quantita_a_ricetta(self):
		self.client().post('/api/ingrediente/', json={'NomeIngrediente': 'Olio'})
		self.client().post('/api/ingrediente/', json={'NomeIngrediente': 'Brodo'})
		self.client().post('/api/ingrediente/', json={'NomeIngrediente': 'Sugo'})
		self.client().post('/api/ricetta/', json={'NomeRicetta': 'Pasta', 'Procedimento': 'fare pasta con olio e sugo'})

		res = self.client().post('/api/ricetta_ingredienti/',
						   json={'NomeRicetta': 'Pasta', 'NomeIngrediente': 'Sugo', 'Quantita': '2'})
		self.assertEqual(200, res.status_code)

		res = self.client().post('/api/ricetta_ingredienti/',
						   json={'NomeRicetta': 'Pasta', 'NomeIngrediente': 'Olio'})
		self.assertEqual(200, res.status_code)

		res = self.client().post('/api/ricetta_ingredienti/',
								 json={'NomeRicetta': 'Capra', 'NomeIngrediente': 'Sesamo'})
		self.assertEqual(404, res.status_code)

	def test_mostra_ingredienti_di_ricetta(self):
		self.test_aggiungi_ingredienti_e_quantita_a_ricetta()
		res = self.client().post('/api/ricetta_ingredienti/', json={'NomeRicetta': 'Pasta'})
		self.assertEqual(200, res.status_code)

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()