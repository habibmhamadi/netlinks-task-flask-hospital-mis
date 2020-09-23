import sys
sys.path.append(".")

from main import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.String())
    patient_name = db.Column(db.String())
    date_registerd = db.Column(db.Date) 

    def __init__(self, doc_id, patient_name, date_registerd):
        self.doc_id = doc_id
        self.patient_name = patient_name
        self.date_registerd = date_registerd

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'doc_id': self.doc_id,
            'patient_name': self.patient_name,
            'date_registered': self.date_registerd
        }