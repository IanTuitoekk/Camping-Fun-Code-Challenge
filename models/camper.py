from models import db
from sqlalchemy.orm import validates

class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # Relationship to signups
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
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
    
    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
        if include_signups:
            data['signups'] = [signup.to_dict() for signup in self.signups]
        return data
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}, Age {self.age}>'