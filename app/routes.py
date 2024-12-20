from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Doctor, Appointment
from datetime import datetime

routes = Blueprint("routes", __name__)

# Home Page
@routes.route("/")
def index():
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    return render_template("index.html", doctors=doctors, appointments=appointments)

# Book an Appointment
@routes.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():
    doctors = Doctor.query.all()

    if request.method == "POST":
        doctor_id = request.form["doctor_id"]
        patient_name = request.form["patient_name"]
        appointment_date = datetime.strptime(request.form["appointment_date"], "%Y-%m-%d").date()
        appointment_time = datetime.strptime(request.form["appointment_time"], "%H:%M").time()

        doctor = Doctor.query.get(doctor_id)

        # Check doctor availability
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).first()

        if existing_appointment:
            # Doctor is unavailable at the selected time
            doctor_appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
            return render_template(
                "book_appointment.html",
                doctors=doctors,
                error="Doctor is already booked at the selected time.",
                doctor_appointments=doctor_appointments,
                selected_doctor=doctor
            )

        # Save the appointment
        new_appointment = Appointment(
            doctor_id=doctor_id,
            patient_name=patient_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for("routes.index"))

    return render_template("book_appointment.html", doctors=doctors, error=None)

@routes.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        available_from = datetime.strptime(request.form["available_from"], "%H:%M").time()
        available_to = datetime.strptime(request.form["available_to"], "%H:%M").time()

        doctor = Doctor(name=name, specialization=specialization, available_from=available_from, available_to=available_to)
        db.session.add(doctor)
        db.session.commit()
        flash("Doctor added successfully!", "success")
        return redirect(url_for("routes.index"))

    return render_template("add_doctor.html")
