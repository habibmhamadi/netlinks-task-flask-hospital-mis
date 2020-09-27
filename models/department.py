import sys
sys.path.append(".")

from sqlalchemy.orm import relationship, backref
from main import db

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    doctors = db.relationship('Doctor', backref='departments', passive_deletes=True, lazy=True)
    date_registerd = db.Column(db.Date)

    def __init__(self, name, date_registerd):
        self.name = name
        self.date_registerd = date_registerd

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'date_registered': self.date_registerd
        }