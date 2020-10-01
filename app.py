import os
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from db import DB
import secrets
import base64
import re
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = DB()

name_regex = re.compile(r'^[a-zA-Z]{1}.*')
present = datetime.now()


def authenticate():
    """Checks if user is logged in
    """
    
    return 'fullname' in session


def admin():
    """Check if user role is admin or normal user
    """
    
    return session['role'] == 'admin'


@app.route("/")
def home():
    """Renders home page with count of each table records
    """
    
    if authenticate():
        apps = db.table('appointments').count()
        deps = db.table('departments').count()
        pats = db.table('patients').count()
        docs = db.table('doctors').count()
        return render_template('index.html', items=[apps, deps, pats, docs])
    return redirect('/login')


@app.route("/appointments")
def appointments():
    """Renders appointments page
    """
    
    if authenticate():
        apps = db.inner_join('appointments', 'doctors',
                             'appointments.doc_id', 'doctors.id')
        docs = db.table('doctors').get()
        return render_template('appointment/index.html', apps=apps, docs=docs)
    return redirect('/login')


@app.route("/appointments/add", methods=['POST', 'GET'])
def add_appointment():
    """Adds a new appointment
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                doc_id = request.form['doctor']
                pat_name = request.form['patient_name']
                pat_lastname = request.form['patient_lastname']
                date = request.form['date']
                time = request.form['time']
                app_date = datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M')
                last_taken = db.table('appointments').get(
                    order='DESC', single=True)
                errs = ''
                if last_taken:
                    if not last_taken['date'] < app_date-timedelta(minutes=1):
                        errs += '- Date must be greater then last appointment.\n'
                elif app_date < present:
                    errs += '- Date must be greater than present.\n'
                if not name_regex.match(pat_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(pat_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/appointments')
                db.table('appointments').add(
                    ('patient_name', 'patient_lastname', 'doc_id', 'date'),
                    (pat_name, pat_lastname, doc_id, date+' '+time))
                return redirect('/appointments')
            return 'Invalid request method!'
        else: return redirect('/appointments')
    return redirect('/login')


@app.route("/appointments/delete/<int:Id>", methods=['GET'])
def delete_appointment(Id):
    """Deletes and specific appointment
    """
    
    if authenticate():
        if admin():
            db.table('appointments').delete('id', Id)
            return redirect('/appointments')
        else: return redirect('/appointments')
    return redirect('/login')


@app.route("/appointments/edit/<int:Id>", methods=['POST'])
def edit_appointment(Id):
    """Edits an specific appointment
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                doc_id = request.form['doctor']
                pat_name = request.form['patient_name']
                pat_lastname = request.form['patient_lastname']
                date = request.form['date']
                time = request.form['time']
                errs = ''
                app_date = datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M')
                errs = ''
                if app_date < present:
                    errs += '- Date should be greater than present.\n'
                if not name_regex.match(pat_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(pat_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/appointments')

                db.table('appointments').update(
                    ('patient_name', 'patient_lastname', 'doc_id', 'date'),
                    (pat_name, pat_lastname, doc_id, date+' '+time),
                    Id
                )
                return redirect('/appointments')
            return redirect('/appointments')
        else: return redirect('/appointments')
    return redirect('/login')


@app.route("/departments")
def departments():
    """Returns departments page
    """
    
    if authenticate():
        deps = db.table('departments').get(order='desc')
        for i in range(len(deps)):
            deps[i] = dict(deps[i])
            docs = db.table('doctors').where(
                'dep_id', deps[i]['id'], single=False)
            deps[i].setdefault('doctors', len(docs))
        return render_template('department/index.html', deps=deps)
    return redirect('/login')


@app.route("/departments/add", methods=['POST', 'GET'])
def add_department():
    """Adds an specific department
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                dep_name = request.form['department']
                if name_regex.match(dep_name):
                    match = db.table('departments').where(
                        'LOWER(dep_name)', dep_name.lower())
                    if match is None:
                        db.table('departments').add(('dep_name', 'dep_date'),
                                                    (dep_name, date.today()))
                        return redirect('/departments')
                    flash('Department '+dep_name+' already exists!')
                    return redirect('/departments')
                flash('Department name should start with letters!')
                return redirect('/departments')
            return redirect('/departments')
        else: return redirect('/departments')
    return redirect('/login')


@app.route("/departments/delete/<int:Id>", methods=['GET'])
def delete_department(Id):
    """Deletes an specific department
    """
    
    if authenticate():
        if admin():
            db.table('departments').delete('id', Id)
            return redirect('/departments')
        else: return redirect('/departments')
    return redirect('/login')


@app.route("/departments/edit/<int:Id>", methods=['POST'])
def edit_department(Id):
    """Edits an specific department
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                dep_name = request.form['department']
                if name_regex.match(dep_name):
                    match = db.table('departments').where(
                        'LOWER(dep_name)', dep_name.lower())
                    if match is None:
                        db.table('departments').update(
                            ('dep_name',), (dep_name,), Id)
                        return redirect('/departments')
                    flash('Department '+dep_name+' already exists!')
                    return redirect('/departments')
                flash('Department name should start with letters!')
                return redirect('/departments')
            return redirect('/departments')
        else: redirect('/departments')
    return redirect('/login')


@app.route("/patients")
def patients():
    """Returns patients page
    """
    
    if authenticate():
        pats = db.table('patients').get()
        return render_template('patient/index.html', pats=pats)
    return redirect('/login')


@app.route("/patients/add", methods=['POST', 'GET'])
def add_patient():
    """Adds an specific patient
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                pat_gender = request.form['gender']
                pat_name = request.form['name']
                pat_lastname = request.form['lastname']
                pat_age = request.form['age']
                errs = ''
                if not name_regex.match(pat_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(pat_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/patients')
                db.table('patients').add(
                    ('p_name', 'p_lastname', 'p_age', 'p_gender', 'p_date'),
                    (pat_name, pat_lastname, pat_age, pat_gender, date.today())
                )
                return redirect('/patients')
            return 'Invalid request method!'
        else: return redirect('/patients')
    return redirect('/login')


@app.route("/patients/delete/<int:Id>", methods=['GET'])
def delete_patient(Id):
    """Deletes an specific patient
    """
    
    if authenticate():
        if admin():
            db.table('patients').delete('id', Id)
            return redirect('/patients')
        else: return redirect('/patients')
    return redirect('/login')


@app.route("/patients/edit/<int:Id>", methods=['POST'])
def edit_patient(Id):
    """Edits an specific patient
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                pat_gender = request.form['gender']
                pat_name = request.form['name']
                pat_lastname = request.form['lastname']
                pat_age = request.form['age']
                errs = ''
                if not name_regex.match(pat_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(pat_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/patients')
                db.table('patients').update(
                    ('p_name', 'p_lastname', 'p_age', 'p_gender'),
                    (pat_name, pat_lastname, pat_age, pat_gender),
                    Id
                )
                return redirect('/patients')
            return redirect('/patients')
        else: return redirect('/patients')
    return redirect('/login')


@app.route("/doctors")
def doctors():
    """Returns doctors page
    """
    
    if authenticate():
        docs = db.inner_join('doctors', 'departments',
                             'doctors.dep_id', 'departments.id')
        deps = db.table('departments').get()
        return render_template('doctor/index.html', docs=docs, deps=deps)
    return redirect('/login')


@app.route("/doctors/add", methods=['POST', 'GET'])
def add_doctor():
    """Adds an specific doctor
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                dep_id = request.form['department']
                doc_name = request.form['name']
                doc_lastname = request.form['lastname']
                doc_details = request.form['details']
                errs = ''
                if not name_regex.match(doc_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(doc_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/doctors')
                db.table('doctors').add(
                    ('doc_name', 'doc_lastname', 'doc_details', 'dep_id', 'doc_date'),
                    (doc_name, doc_lastname, doc_details, dep_id, date.today())
                )
                return redirect('/doctors')
            return 'Invalid request method!'
        return redirect('/doctors')
    return redirect('/login')


@app.route("/doctors/delete/<int:Id>", methods=['GET'])
def delete_doctor(Id):
    """Deletes an specific doctor
    """
    
    if authenticate():
        if admin():
            db.table('doctors').delete('id', Id)
            return redirect('/doctors')
        else: return redirect('/doctors')
    return redirect('/login')


@app.route("/doctors/edit/<int:Id>", methods=['POST'])
def edit_doctor(Id):
    """Edits an specific doctor
    """
    
    if authenticate():
        if admin():
            if request.method == 'POST':
                dep_id = request.form['department']
                doc_name = request.form['name']
                doc_lastname = request.form['lastname']
                doc_details = request.form['details']
                errs = ''
                if not name_regex.match(doc_name):
                    errs += '- Name should start with letters.\n'
                if not name_regex.match(doc_lastname):
                    errs += '- Lastname should start with letters.'
                if len(errs) > 0:
                    flash(errs)
                    return redirect('/doctors')
                db.table('doctors').update(
                    ('doc_name', 'doc_lastname', 'doc_details', 'dep_id'),
                    (doc_name, doc_lastname, doc_details, dep_id),
                    Id
                )
                return redirect('/doctors')
            return redirect('/doctors')
        else: return redirect('/doctors')
    return redirect('/login')


@app.route("/login", methods=['POST', 'GET'])
def login():
    """Returns login page
    """
    
    if authenticate():
        return redirect('/')
    if request.method == 'POST':
        eml = request.form['email']
        pwd = request.form['password']
        pwd = base64.b64encode(pwd.encode("utf-8"))
        res = db.table('auths').where_and('email', 'password', (eml, str(pwd)))
        if res is None:
            flash('Incorrect credentials')
            return redirect('/login')
        else:
            session['fullname'] = res['fullname']
            session['role'] = res['role']
            return redirect('/')
    return render_template('auth/login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Returns register page
    """
    
    if authenticate():
        return redirect('/')
    if request.method == 'POST':
        fname = request.form['fullname']
        eml = request.form['email']
        pwd = request.form['password']
        pwd = base64.b64encode(pwd.encode("utf-8"))
        res = db.table('auths').where('email', eml)
        if res is None:
            db.table('auths').add(('fullname', 'email', 'password', 'role'),
                                  (fname, eml, str(pwd), 'user'))
            session['fullname'] = fname
            session['role'] = 'user'
            return redirect('/')
        else:
            flash('Email has already taken!')
            return redirect('/register')
    return render_template('auth/register.html')


@app.route("/logout")
def logout():
    """Logouts from session
    """
    
    if authenticate():
        session.pop('fullname', None)
        session.pop('role', None)
        return redirect('/login')
    return render_template('/login')


@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def catch_all(path):
    """Catches all routes and returns 404 if url does not much
    """
    
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
