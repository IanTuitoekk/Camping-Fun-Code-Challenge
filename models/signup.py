from models import db
from dataclasses import dataclass
from sqlalchemy.orm import validates

# a type to represent the signup data
@dataclass
class SignupType:
    id: int
    camper_id: int
    activity_id: int
    time: int

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    
    # Relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    def __init__(self, camper_id, activity_id, time):
        self.camper_id = camper_id
        self.activity_id = activity_id
        self.time = time
    
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 23:
            raise ValueError("Time must be between 0 and 23")
        return time