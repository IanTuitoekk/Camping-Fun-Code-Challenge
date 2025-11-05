from models import db

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    # Relationship to signups with cascade delete
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty
        }
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}, Difficulty {self.difficulty}>'