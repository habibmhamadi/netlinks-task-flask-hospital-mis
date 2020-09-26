import os
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import secrets
import base64
import re
from datetime import date

app = Flask(__name__, static_url_path='', 
            static_folder='static',)
app.secret_key = secrets.token_urlsafe(16)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department
from models.auth import Auth

name_regex = re.compile(r'^[a-zA-Z]{1}.*')

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
        deps = Department.query.all()
        return render_template('department/index.html',deps=deps)
    return redirect('/login')

@app.route("/departments/add",methods=['POST','GET'])
def add_department():
    if authenticate():
        if request.method == 'POST':
            dep_name = request.form['department']
            if name_regex.match(dep_name):
                query = Department.query.filter(func.lower(Department.name)==func.lower(dep_name)).first()
                if query is None:
                    new_dep = Department(
                        name=dep_name,
                        date_registerd=date.today()
                    )
                    db.session.add(new_dep)
                    db.session.commit()
                    return redirect('/departments')
                flash('Department '+dep_name+' already exists!')
                return redirect('/departments')
            flash('Department name should start with letters!')
            return redirect('/departments')
        return 'Invalid request method!'
    return redirect('/login')

@app.route("/patients")
def patients():
    if authenticate():
        pats = Patient.query.all()
        return render_template('patient/index.html',pats=pats)
    return redirect('/login')

@app.route("/doctors")
def doctors():
    if authenticate():
        docs = Doctor.query.all()
        deps = Department.query.all()
        return render_template('doctor/index.html',docs=docs,deps=deps)
    return redirect('/login')

@app.route("/doctors/add",methods=['POST','GET'])
def add_doctor():
    if authenticate():
        if request.method == 'POST':
            dep_id = request.form['department']
            doc_name = request.form['name']
            doc_lastname = request.form['lastname']
            doc_details = request.form['details']
            errs = ''
            if not name_regex.match(doc_name):
                errs +='- Name should start with letters.\n'
            if not name_regex.match(doc_lastname):
                errs +='- Lastname should start with letters.'
            if len(errs)>0:
                flash(errs)
                return redirect('/doctors')
            new_doc = Doctor(
                name=doc_name,
                lastname=doc_lastname,
                details=doc_details,
                dep_id=dep_id,
                date_registerd=date.today()
            )
            db.session.add(new_doc)
            db.session.commit()
            return redirect('/doctors')
        return 'Invalid request method!'
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