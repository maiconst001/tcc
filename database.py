from flask_sqlalchemy import SQLAlchemy, model
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    verified_acount = db.Column(db.Boolean, nullable=False)


    # parte das cores
    def __repr__(self):
        return f'user: {self.username}'




class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    nome = db.Column(db.String(120), nullable=False)
    horarios = db.Column(db.String(40), nullable=False)
    lab = db.Column(db.String(10), nullable=False)
    data = db.Column(db.String(120), nullable=False)


    
    def __repr__(self):
        return f'agenda: {self.data}'



class Labs(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(70), nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    
    def __repr__(self):
        return f'agenda: {self.data}'



def db_init(app):
    app.db = db
    db.init_app(app)