from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    available_from = db.Column(db.Time, nullable=False)
    available_to = db.Column(db.Time, nullable=False)

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("Doctor", backref="appointments")
