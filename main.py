import os
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets

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


def authenticate(request_url):
    if 'email' in session:
        return render_template(request_url)
    return redirect('login')
    
def guest(request_url):
    if 'email' in session:
        return redirect('/')
    return render_template(request_url)
    

@app.route("/")
def home():
    return authenticate('index.html')

@app.route("/appointments")
def appointments():
    return authenticate('appointments.html')

@app.route("/departments")
def departments():
    return authenticate('departments.html')

@app.route("/patients")
def patients():
    return authenticate('patients.html')

@app.route("/doctors")
def doctors():
    return authenticate('doctors.html')

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method =='POST':
        eml = request.form['email']
        pwd = request.form['password']
        a = Auth.query.filter_by(email=eml).filter_by(password=pwd).first()
        return 'None' if a==None else Auth.serialize(a)
    #     if request.form['email'] == 'habib@gmail.com':
    #         session['email'] = request.form['email']
    #         return redirect('/')
    #     else:
    #         flash('Incorrect credentials')
    #         return redirect('/login')
    elif request.method == 'GET':
        return guest('auth/login.html')
    # return 'Invalid route method'

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method =='POST':
        session['email'] = request.form['email']
        return redirect('/')
    elif request.method == 'GET':
        return guest('auth/register.html')
    return 'Invalid route method'

@app.route("/logout", methods=['GET'])
def logout():
    if request.method =='GET':
        session.pop('email', None)
        return redirect('/')
    return 'Invalid route method'

    
# if __name__ == "__main__":
#     app.run(debug=True)