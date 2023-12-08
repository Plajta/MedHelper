from flask_login import UserMixin
from . import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    placement = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, unique=True)

class Messages(db.Model):
    sender_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
