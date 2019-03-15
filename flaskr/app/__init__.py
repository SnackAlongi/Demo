from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
	from app.models import Ricetta, Ingrediente, Ricetta_Ingrediente
	app = FlaskAPI(__name__,static_folder = "../../dist/static",
					template_folder = "../../dist", instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/ricetta/', methods=['POST'])
	def aggiungi_ricetta():
		if request.method == "POST":
			nome = str(request.data.get('NomeRicetta', ''))
			procedimento = str(request.data.get('Procedimento', ''))

			if nome and procedimento:
				ricetta = Ricetta(nome_ricetta=nome, procedimento=procedimento)
				ricetta.save()
				response = jsonify({
					'NomeRicetta': ricetta.nome_ricetta,
					'Procedimento': ricetta.procedimento
				})
				response.status_code = 201
				return response
		else:
			return abort(404)

	@app.route('/ricetta/', methods=['GET'])
	def mostra_ricette():
		if request.method == "GET":
			ricette = Ricetta.get_all()
			results = []

			for ricetta in ricette:
				r = {
					'NomeRicetta': ricetta.nome_ricetta,
					'Procedimento': ricetta.procedimento
				}
				results.append(r)

			response = jsonify(results)
			response.status_code = 200
			return response
		else:
			return abort(404)

	@app.route('/mostra/', methods=['POST'])
	def mostra_ricetta():
		if request.method == 'POST':
			nome = request.data.get('NomeRicetta')
			if Ricetta.get_ricetta(nome):
				ricetta = Ricetta.get_ricetta(nome)
				response = jsonify({
					'NomeRicetta': ricetta.nome_ricetta,
					'Procedimento': ricetta.procedimento
				})
				response.status_code = 200
				return response
			else:
				return abort(404)
		else:
			return abort(404)


	@app.route('/ingrediente/', methods=['POST'])
	def aggiungi_ingrediente():
		if request.method == "POST":
			nome = str(request.data.get('NomeIngrediente', ''))

			if nome:
				ingrediente = Ingrediente(nome_ingrediente=nome)
				ingrediente.save()
				response = jsonify({
					'NomeIngrediente': ingrediente.nome_ingrediente,
				})
				response.status_code = 201
				return response
		else:
			abort(404)

	@app.route('/ingrediente/', methods=['GET'])
	def mostra_ingredienti():
		if request.method == "GET":
			ingredienti = Ingrediente.get_all()
			results = []

			for ingrediente in ingredienti:
				i = {
					'NomeIngrediente': ingrediente.nome_ingrediente,
				}
				results.append(i)

			response = jsonify(results)
			response.status_code = 200
			return response
		else:
			abort(404)

	@app.route('/ricetta_ingredienti/', methods=['POST'])
	def aggiungi_e_mostra_ingredienti_di_ricetta():
		if request.method == 'POST':
			nomeRicetta = request.data.get('NomeRicetta')
			nomeIngrediente = request.data.get('NomeIngrediente')
			quantita = request.data.get('Quantita')

			if Ricetta.get_ricetta(nomeRicetta) and Ingrediente.get_ingrediente(nomeIngrediente):
				if quantita is None: quantita = 1

				ricetta_ingrediente = Ricetta_Ingrediente(ricetta_id=nomeRicetta, ingrediente_id=nomeIngrediente, quantita=quantita)
				ricetta_ingrediente.save()
				response = jsonify({
					'NomeRicetta': ricetta_ingrediente.ricetta_id,
					'NomeIngrediente': ricetta_ingrediente.ingrediente_id,
					'Quantita': ricetta_ingrediente.quantita
				})
				response.status_code = 200
				return response

			elif Ricetta.get_ricetta(nomeRicetta) and Ingrediente.get_ingrediente(nomeIngrediente) is None:
				ingredienti = Ricetta_Ingrediente.get_ingredienti_di_ricetta(nomeRicetta)

				results = []
				for ingrediente in ingredienti:
					i = {
						'NomeIngrediente': ingrediente.ingrediente_id,
						'Quantita': ingrediente.quantita
					}
					results.append(i)
				response = jsonify(results)
				response.status_code = 200
				return response

			else:
				abort(404, 'La ricetta o l''ingrediente non sono presenti ')

		else:
			#GET
			abort(404)
	return app
