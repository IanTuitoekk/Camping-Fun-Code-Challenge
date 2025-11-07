from models import db
from dataclasses import dataclass

# a type to represent the activity data
@dataclass
class ActivityType:
    id: int
    name: str
    difficulty: int

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    # Relationship to signups with cascade delete
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty