from models.activity import Activity, ActivityType
from models import db

def get_all_activities() -> list[ActivityType]:
    activities = Activity.query.all()  # SELECT * FROM activities
    return [ActivityType(id=a.id, name=a.name, difficulty=a.difficulty) for a in activities]

def delete_activity(activity_id: int) -> bool:
    activity = Activity.query.get(activity_id)
    if activity:
        db.session.delete(activity)  # DELETE FROM activities WHERE id = activity_id (cascade deletes signups)
        db.session.commit()
        return True
    return False