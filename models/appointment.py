import sys
sys.path.append(".")
from sqlalchemy.orm import relationship, backref
from main import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String())
    patient_lastname = db.Column(db.String())
    doc_id = db.Column(db.Integer, db.ForeignKey('doctors.id',ondelete='CASCADE'))
    date_registerd = db.Column(db.DateTime) 

    def __init__(self, doc_id, patient_name, patient_lastname, date_registerd):
        self.doc_id = doc_id
        self.patient_name = patient_name
        self.patient_lastname = patient_lastname
        self.date_registerd = date_registerd

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'doc_id': self.doc_id,
            'patient_name': self.patient_name,
            'patient_lastname':self.patient_lastname,
            'date_registered': self.date_registerd
        }