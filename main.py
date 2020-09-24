import os
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import base64

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department
from models.auth import Auth


def authenticate():
    return 'fullname' in session
    
@app.route("/")
def home():
    if authenticate():
        apps = Appointment.query.all()
        deps = Department.query.all()
        pats = Patient.query.all()
        docs = Doctor.query.all()
        return render_template('index.html',items=[
            len(apps),
            len(deps),
            len(pats),
            len(docs)
        ])
    return redirect('/login')

@app.route("/appointments")
def appointments():
    if authenticate():
        apps = Appointment.query.all()
        return render_template('appointment/index.html',apps=apps)
    return redirect('/login')

@app.route("/departments")
def departments():
    if authenticate():
        deps = Appointment.query.all()
        return render_template('department/index.html',deps=deps)
    return redirect('/login')

@app.route("/patients")
def patients():
    if authenticate():
        pats = Appointment.query.all()
        return render_template('patient/index.html',pats=pats)
    return redirect('/login')

@app.route("/doctors")
def doctors():
    if authenticate():
        docs = Appointment.query.all()
        return render_template('doctor/index.html',docs=docs)
    return redirect('/login')

@app.route("/login", methods=['POST','GET'])
def login():
    if authenticate():
        return redirect('/')
    if request.method =='POST':
        eml = request.form['email']
        pwd = request.form['password']
        pwd = base64.b64encode(pwd.encode("utf-8"))
        res = Auth.query.filter_by(email=eml).filter_by(password=str(pwd)).first()
        if res is None:
            flash('Incorrect credentials')
            return redirect('/login')
        else:
            session['fullname'] = res.fullname
            return redirect('/')
    return render_template('auth/login.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if authenticate():
        return redirect('/')
    if request.method =='POST':
        fname = request.form['fullname']
        eml = request.form['email']
        pwd = request.form['password']
        pwd = base64.b64encode(pwd.encode("utf-8"))
        res = Auth.query.filter_by(email=eml).first()
        if res is None:
            newAuth = Auth(
                fullname = fname,
                email = eml,
                password = str(pwd)
            )
            db.session.add(newAuth)
            db.session.commit()
            session['fullname'] = fname
            return redirect('/')
        else: 
            flash('Email has already taken!')
            return redirect('/register')
    return render_template('auth/register.html')

@app.route("/logout")
def logout():
    if authenticate():
        session.pop('fullname', None)
        return redirect('/login')
    return render_template('/login')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def page_not_found(path):
    return render_template('404.html')

    
# if __name__ == "__main__":
#     app.run(debug=True)