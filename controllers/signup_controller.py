from models.signup import Signup, SignupType
from models.camper import Camper
from models.activity import Activity
from models import db

def create_signup(camper_id: int, activity_id: int, time: int) -> dict | None:
    # Validate camper exists
    camper = Camper.query.get(camper_id)
    if not camper:
        return {"errors": ["Camper not found"]}
    
    # Validate activity exists
    activity = Activity.query.get(activity_id)
    if not activity:
        return {"errors": ["Activity not found"]}
    
    try:
        new_signup = Signup(camper_id=camper_id, activity_id=activity_id, time=time)
        db.session.add(new_signup)  # INSERT INTO signups (camper_id, activity_id, time) VALUES (...)
        db.session.commit()
        
        # Return signup with nested camper and activity
        return {
            'id': new_signup.id,
            'camper_id': new_signup.camper_id,
            'activity_id': new_signup.activity_id,
            'time': new_signup.time,
            'camper': {
                'id': new_signup.camper.id,
                'name': new_signup.camper.name,
                'age': new_signup.camper.age
            },
            'activity': {
                'id': new_signup.activity.id,
                'name': new_signup.activity.name,
                'difficulty': new_signup.activity.difficulty
            }
        }
    except ValueError as e:
        db.session.rollback()
        return {"errors": [str(e)]}