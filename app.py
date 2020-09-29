import os
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from db import DB
import secrets
import base64
import re
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = DB()

name_regex = re.compile(r'^[a-zA-Z]{1}.*')

def authenticate():
    return 'fullname' in session
    
@app.route("/")
def home():
    if authenticate():
        apps = db.table('appointments').count()
        deps = db.table('departments').count()
        pats = db.table('patients').count()
        docs = db.table('doctors').count()
        return render_template('index.html',items=[apps,deps,pats,docs])
    return redirect('/login')

@app.route("/appointments")
def appointments():
    if authenticate():
        apps = db.table('appointments').all()
        docs = db.table('doctors').all()
        return render_template('appointment/index.html',apps=apps,docs=docs)
    return redirect('/login')

@app.route("/appointments/add",methods=['POST','GET'])
def add_appointment():
    if authenticate():
        if request.method == 'POST':
            doc_id = request.form['doctor']
            pat_name = request.form['patient_name']
            pat_lastname = request.form['patient_lastname']
            date = request.form['date']
            time = request.form['time']
            errs = ''
            if not name_regex.match(pat_name):
                errs +='- Name should start with letters.\n'
            if not name_regex.match(pat_lastname):
                errs +='- Lastname should start with letters.'
            if len(errs)>0:
                flash(errs)
                return redirect('/appointments')
            db.table('appointments').add(
                ('patient_name','patient_lastname','doc_id','date_registerd'),
                (pat_name,pat_lastname,doc_id,date+' '+time))
            return redirect('/appointments')
        return 'Invalid request method!'
    return redirect('/login')

@app.route("/appointments/delete/<int:Id>",methods=['GET'])
def delete_appointment(Id):
    if authenticate():
        db.table('appointments').delete('id',Id)
        return redirect('/appointments')
    return redirect('/login')

@app.route("/appointments/edit/<int:Id>",methods=['POST'])
def edit_appointment(Id):
    if authenticate():
        if request.method == 'POST':
            doc_id = request.form['doctor']
            pat_name = request.form['patient_name']
            pat_lastname = request.form['patient_lastname']
            date = request.form['date']
            time = request.form['time']
            errs = ''
            if not name_regex.match(pat_name):
                errs +='- Name should start with letters.\n'
            if not name_regex.match(pat_lastname):
                errs +='- Lastname should start with letters.'
            if len(errs)>0:
                flash(errs)
                return redirect('/appointments')
            
            db.table('appointments').update(
                ('name','lastname','dep_id','date_registerd'),
                (pat_name,pat_lastname,doc_id,date+' '+time),
                Id
            )
            return redirect('/appointments')
        return redirect('/appointments')
    return redirect('/login')

@app.route("/departments")
def departments():
    if authenticate():
        deps = db.table('departments').all(order_by='desc')
        return render_template('department/index.html',deps=deps)
    return redirect('/login')

@app.route("/departments/add",methods=['POST','GET'])
def add_department():
    if authenticate():
        if request.method == 'POST':
            dep_name = request.form['department']
            if name_regex.match(dep_name):
                match = db.table('departments').where('LOWER(name)',dep_name.lower())
                if match is None:
                    db.table('departments').add(('name','date_registerd'),
                                                (dep_name,date.today()))
                    return redirect('/departments')
                flash('Department '+dep_name+' already exists!')
                return redirect('/departments')
            flash('Department name should start with letters!')
            return redirect('/departments')
        return redirect('/departments')
    return redirect('/login')

@app.route("/departments/delete/<int:Id>",methods=['GET'])
def delete_department(Id):
    if authenticate():
        db.table('departments').delete('id',Id)
        return redirect('/departments')
    return redirect('/login')

@app.route("/departments/edit/<int:Id>",methods=['POST'])
def edit_department(Id):
    if authenticate():
        if request.method == 'POST':
            dep_name = request.form['department']
            if name_regex.match(dep_name):
                match = db.table('departments').where('LOWER(name)',dep_name.lower())
                if match is None:
                    db.table('departments').update(('name',),(dep_name,),Id)
                    return redirect('/departments')
                flash('Department '+dep_name+' already exists!')
                return redirect('/departments')
            flash('Department name should start with letters!')
            return redirect('/departments')
        return redirect('/departments')
    return redirect('/login')

@app.route("/patients")
def patients():
    if authenticate():
        pats = db.table('patients').all()
        return render_template('patient/index.html',pats=pats)
    return redirect('/login')

@app.route("/patients/add",methods=['POST','GET'])
def add_patient():
    if authenticate():
        if request.method == 'POST':
            pat_gender = request.form['gender']
            pat_name = request.form['name']
            pat_lastname = request.form['lastname']
            pat_age = request.form['age']
            errs = ''
            if not name_regex.match(pat_name):
                errs +='- Name should start with letters.\n'
            if not name_regex.match(pat_lastname):
                errs +='- Lastname should start with letters.'
            if len(errs)>0:
                flash(errs)
                return redirect('/patients')
            db.table('patients').add(
                ('name','lastname','age','gender','date_registerd'),
                (pat_name,pat_lastname,pat_age,pat_gender,date.today())
            )
            return redirect('/patients')
        return 'Invalid request method!'
    return redirect('/login')

@app.route("/patients/delete/<int:Id>",methods=['GET'])
def delete_patient(Id):
    if authenticate():
        db.table('patients').delete('id',Id)
        return redirect('/patients')
    return redirect('/login')

@app.route("/patients/edit/<int:Id>",methods=['POST'])
def edit_patient(Id):
    if authenticate():
        if request.method == 'POST':
            pat_gender = request.form['gender']
            pat_name = request.form['name']
            pat_lastname = request.form['lastname']
            pat_age = request.form['age']
            errs = ''
            if not name_regex.match(pat_name):
                errs +='- Name should start with letters.\n'
            if not name_regex.match(pat_lastname):
                errs +='- Lastname should start with letters.'
            if len(errs)>0:
                flash(errs)
                return redirect('/patients')
            db.table('patients').update(
                ('name','lastname','age','gender'),
                (pat_name,pat_lastname,pat_age,pat_gender),
                Id
            )
            return redirect('/patients')
        return redirect('/patients')
    return redirect('/login')


@app.route("/doctors")
def doctors():
    if authenticate():
        docs = db.inner_join('doctors','departments','doctors.dep_id','departments.id')
        deps = db.table('departments').all()    
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
            db.table('doctors').add(
                ('name','lastname','details','dep_id','date_registerd'),
                (doc_name,doc_lastname,doc_details,dep_id,date.today())
            )
            return redirect('/doctors')
        return 'Invalid request method!'
    return redirect('/login')

@app.route("/doctors/delete/<int:Id>",methods=['GET'])
def delete_doctor(Id):
    if authenticate():
        db.table('doctors').delete('id',Id)
        return redirect('/doctors')
    return redirect('/login')

@app.route("/doctors/edit/<int:Id>",methods=['POST'])
def edit_doctor(Id):
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
            db.table('doctors').update(
                ('name','lastname','details','dep_id'),
                (doc_name,doc_lastname,doc_details,dep_id),
                Id
            )
            return redirect('/doctors')
        return redirect('/doctors')
    return redirect('/login')

@app.route("/login", methods=['POST','GET'])
def login():
    if authenticate():
        return redirect('/')
    if request.method =='POST':
        eml = request.form['email']
        pwd = request.form['password']
        pwd = base64.b64encode(pwd.encode("utf-8"))
        res = db.table('auths').where_and('email','password',(eml,str(pwd)))
        if res is None:
            flash('Incorrect credentials')
            return redirect('/login')
        else:
            session['fullname'] = res['fullname']
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
        res = db.table('auths').where('email',eml)
        if res is None:
            db.table('auths').add(('fullname','email','password'),
                                  (fname,eml,str(pwd)))
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

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def catch_all(path):
    return render_template('404.html')

    
if __name__ == "__main__":
    app.run(debug=True)