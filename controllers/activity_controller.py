from flask import Blueprint, jsonify
from models import db
from models.activity import Activity

activity_bp = Blueprint('activities', __name__, url_prefix='/activities')

@activity_bp.route('', methods=['GET'])
def get_activities():
    """Get all activities"""
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

@activity_bp.route('/<int:id>', methods=['DELETE'])
def delete_activity(id):
    """Delete an activity and cascade delete its signups"""
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return '', 204