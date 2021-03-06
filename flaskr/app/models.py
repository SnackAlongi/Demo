from app import db
from instance.config import Config
from flask_security import RoleMixin, UserMixin
from datetime import datetime, timedelta
import jwt

class Ricetta_Ingrediente(db.Model):
    __tablename__ = 'ricetta_ingrediente'
    ricetta_id = db.Column(db.Integer, db.ForeignKey('ricetta.nome_ricetta'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.nome_ingrediente'), primary_key=True)
    quantita = db.Column(db.Integer())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_ingredienti_di_ricetta(nome):
        return Ricetta_Ingrediente.query.filter_by(ricetta_id=nome).all()

class Ricetta(db.Model):
    __tablename__ = 'ricetta'
    nome_ricetta = db.Column(db.String(80), primary_key=True)
    procedimento = db.Column(db.String(255))

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


    def __str__(self):
        return self.nome_ingrediente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Ingrediente.query.all()

    @staticmethod
    def get_ingrediente(nome):
        return Ingrediente.query.filter_by(nome_ingrediente = nome).first()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=15, seconds=0),
                'iat': datetime.utcnow(),
                'sub': self.email
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

