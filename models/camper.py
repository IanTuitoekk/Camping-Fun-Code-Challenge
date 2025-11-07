from models import db
from dataclasses import dataclass
from sqlalchemy.orm import validates

# a type to represent the camper data
@dataclass
class CamperType:
    id: int
    name: str
    age: int

class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # Relationship to signups
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Name is required")
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age < 8 or age > 18:
            raise ValueError("Age must be between 8 and 18")
        return age