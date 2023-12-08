from flask_login import UserMixin
from . import db

class Doctor(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100))
    displayname = db.Column(db.String(1000))
    rank = db.Column(db.String(32))
    level = db.Column(db.Integer)

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    birth = db.Column(db.String(16))
    name = db.Column(db.String(255))

class Placement(db.Model): 
    id = db.Column(db.String(36), primary_key=True, unique=True)
    placement = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, unique=True)

class Messages(db.Model):
    sender_id = db.Column(db.String(36), primary_key=True)
    body = db.Column(db.Text)
