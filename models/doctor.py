import sys
sys.path.append(".")

from sqlalchemy.orm import relationship, backref
from main import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    details = db.Column(db.String())
    dep_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    # departments = relationship("Department", backref=backref("departments", uselist=False))
    date_registerd = db.Column(db.Date) 

    def __init__(self, name, lastname, details, dep_id, date_registerd):
        self.name = name
        self.lastname = lastname
        self.details = details
        self.date_registerd = date_registerd
        self.dep_id = dep_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'lastname': self.lastname,
            'details': self.details,
            'dep_id': self.dep_id,
            'date_registered': self.date_registerd
        }