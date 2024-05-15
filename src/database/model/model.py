from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Temperatura(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    local = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Double, nullable= False)

class Umidade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    local = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Double, nullable= False)

class Solo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    local = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Double, nullable= False)
