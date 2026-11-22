import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://", 1

    )

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


ATTENDANCE_PASSWORD = "mora123"


class StudentAttendance(db.Model):
    __tablename__ = "student_attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20))
    student_name = db.Column(db.String(100))
    attendance = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.student_name


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        student_id = request.form["student_id"]
        student_name = request.form["student_name"]
        password = request.form["password"]

        if password != ATTENDANCE_PASSWORD:
            message = "Wrong Attendance Password!"
            return render_template("home1.html", message=message)

        student = StudentAttendance.query.filter_by(
            student_id=student_id
        ).first()

        if student:
            student.attendance += 1
        else:
            student = StudentAttendance(
                student_id=student_id,
                student_name=student_name,
                attendance=1
            )
            db.session.add(student)

        db.session.commit()

        message = "Attendance Added Successfully!"

    return render_template("home1.html", message=message)


@app.route("/records")
def records():

    students = StudentAttendance.query.all()

    return render_template(
        "records1.html",
        students=students
    )


@app.route("/graph")
def graph():

    students = StudentAttendance.query.all()

    labels = [s.student_name for s in students]
    values = [s.attendance for s in students]

    return render_template(
        "graph.html",
        labels=labels,
        values=values
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
