import sys
sys.path.append(".")

from main import db

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    date_registerd = db.Column(db.Date) 

    def __init__(self, name, lastname, age, gender, date_registerd):
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.date_registerd = date_registerd
        self.age = age

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender,
            'date_registered': self.date_registerd
        }