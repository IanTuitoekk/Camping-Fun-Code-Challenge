from models.camper import Camper, CamperType
from models import db

def get_all_campers() -> list[CamperType]:
    campers = Camper.query.all()  # SELECT * FROM campers
    return [CamperType(id=c.id, name=c.name, age=c.age) for c in campers]

def get_camper_by_id(camper_id: int) -> dict | None:
    camper = Camper.query.get(camper_id)  # SELECT * FROM campers WHERE id = camper_id
    if camper:
        # Return camper with signups (each signup nests activity)
        return {
            'id': camper.id,
            'name': camper.name,
            'age': camper.age,
            'signups': [
                {
                    'id': signup.id,
                    'camper_id': signup.camper_id,
                    'activity_id': signup.activity_id,
                    'time': signup.time,
                    'activity': {
                        'id': signup.activity.id,
                        'name': signup.activity.name,
                        'difficulty': signup.activity.difficulty
                    }
                }
                for signup in camper.signups
            ]
        }
    return None

def create_camper(name: str, age: int) -> CamperType | dict:
    try:
        new_camper = Camper(name=name, age=age)
        db.session.add(new_camper)  # INSERT INTO campers (name, age) VALUES (...)
        db.session.commit()
        return CamperType(id=new_camper.id, name=new_camper.name, age=new_camper.age)
    except ValueError as e:
        db.session.rollback()
        return {"errors": [str(e)]}

def update_camper(camper_id: int, name: str | None = None, age: int | None = None) -> CamperType | dict | None:
    camper = Camper.query.get(camper_id)
    if camper:
        try:
            if name is not None:
                camper.name = name
            if age is not None:
                camper.age = age
            db.session.commit()  # UPDATE campers SET ... WHERE id = camper_id
            return CamperType(id=camper.id, name=camper.name, age=camper.age)
        except ValueError as e:
            db.session.rollback()
            return {"errors": [str(e)]}
    return None