from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
	from app.models import Ricetta, Ingrediente
	app = FlaskAPI(__name__,static_folder = "../../dist/static",
					template_folder = "../../dist", instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/ricette/', methods=['POST'])
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

	@app.route('/ricette/', methods=['GET'])
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

	return app
