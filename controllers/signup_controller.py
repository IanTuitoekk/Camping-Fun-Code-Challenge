from flask import request, jsonify
from models import db
from models.signup import Signup
from models.camper import Camper
from models.activity import Activity

def register_signup_routes(app):
    
    @app.route('/signups', methods=['POST'])
    def create_signup():
        """Create a new signup"""
        data = request.get_json()
        
        camper_id = data.get('camper_id')
        activity_id = data.get('activity_id')
        
        if not camper_id or not activity_id:
            return jsonify({"errors": ["camper_id and activity_id are required"]}), 400
        
        camper = Camper.query.get(camper_id)
        activity = Activity.query.get(activity_id)
        
        if not camper:
            return jsonify({"errors": ["Camper not found"]}), 400
        if not activity:
            return jsonify({"errors": ["Activity not found"]}), 400
        
        try:
            signup = Signup(
                camper_id=camper_id,
                activity_id=activity_id,
                time=data.get('time')
            )
            
            db.session.add(signup)
            db.session.commit()
            
            return jsonify(signup.to_dict()), 201
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400