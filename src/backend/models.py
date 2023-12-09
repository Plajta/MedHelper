from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db

class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctors'
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100))
    displayname = db.Column(db.String(1000))
    rank = db.Column(db.String(32))
    level = db.Column(db.Integer)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    birth = db.Column(db.String(16))
    name = db.Column(db.String(255))
    placement_id = db.Column(db.String(36), unique=True)

    def __repr__(self):
        return f"<Patient {self.id} on {self.placement_id}>"

class Placement(db.Model):
    __tablename__ = 'placements'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    placement = db.Column(db.String(255))

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("patients.id"))
    body = db.Column(db.Text)
    response = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    patient = relationship("Patient", back_populates = "messages")

    def __repr__(self):
        return f"<Message {self.id} by {self.patient}>"

class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("patients.id"))
    answers = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    patient = relationship("Patient", back_populates = "questionnaires")

    def __repr__(self):
        return f"<Questionnaire {self.id} by {self.patient}>"


Patient.messages = relationship("Message", order_by = Message.timestamp, back_populates = "patient")
Patient.questionnaires = relationship("Questionnaire", order_by = Questionnaire.timestamp, back_populates = "patient")