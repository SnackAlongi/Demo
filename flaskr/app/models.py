from app import db
#from flask_sqlalchemy import SQLAlchemy

class Ricetta_Ingrediente(db.Model):
    __tablename__ = 'ricetta_ingrediente'
    ricetta_id = db.Column(db.Integer, db.ForeignKey('ricetta.nome_ricetta'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.nome_ingrediente'), primary_key=True)
    quatita = db.Column(db.Integer())

class Ricetta(db.Model):
    __tablename__ = 'ricetta'
    nome_ricetta = db.Column(db.String(80), primary_key=True)
    procedimento = db.Column(db.String(255))
    #ingrediente = db.relationship("Ricetta_Ingrediente", back_populates='ricetta')

    def __str__(self):
        return self.nome_ricetta

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Ricetta.query.all()

    @staticmethod
    def get_ricetta(nome):
        return Ricetta.query.filter_by(nome_ricetta = nome).first()

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    nome_ingrediente = db.Column(db.String(255), primary_key=True)
    #ricetta= db.relationship("Ricetta_Ingrediente", back_populates='ingrediente')

    def __str__(self):
        return self.nome_ingrediente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Ingrediente.query.all()