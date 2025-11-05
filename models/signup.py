from models import db
from sqlalchemy.orm import validates

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    
    # Relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 23:
            raise ValueError("Time must be between 0 and 23")
        return time
    
    def to_dict(self):
        return {
            'id': self.id,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id,
            'time': self.time,
            'activity': self.activity.to_dict(),
            'camper': self.camper.to_dict()
        }
    
    def __repr__(self):
        return f'<Signup {self.id}: Camper {self.camper_id} -> Activity {self.activity_id} at {self.time}:00>'