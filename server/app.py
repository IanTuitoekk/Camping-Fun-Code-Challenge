from flask import Flask, request, jsonify
from models import db
from flask_migrate import Migrate
from server.config import Config

# Import controller functions (not route registration functions)
from controllers.activity_controller import get_all_activities, delete_activity
from controllers.camper_controller import get_all_campers, get_camper_by_id, create_camper, update_camper
from controllers.signup_controller import create_signup

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Activity Routes
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = get_all_activities()
    return jsonify([{'id': a.id, 'name': a.name, 'difficulty': a.difficulty} for a in activities]), 200

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity_route(id):
    if delete_activity(id):
        return '', 204
    return jsonify({"error": "Activity not found"}), 404

# Camper Routes
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = get_all_campers()
    return jsonify([{'id': c.id, 'name': c.name, 'age': c.age} for c in campers]), 200

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = get_camper_by_id(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify(camper), 200

@app.route('/campers', methods=['POST'])
def create_camper_route():
    data = request.get_json()
    result = create_camper(data.get('name'), data.get('age'))
    
    if isinstance(result, dict) and 'errors' in result:
        return jsonify(result), 400
    
    return jsonify({'id': result.id, 'name': result.name, 'age': result.age}), 201

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper_route(id):
    data = request.get_json()
    result = update_camper(id, data.get('name'), data.get('age'))
    
    if result is None:
        return jsonify({"error": "Camper not found"}), 404
    
    if isinstance(result, dict) and 'errors' in result:
        return jsonify(result), 400
    
    return jsonify({'id': result.id, 'name': result.name, 'age': result.age}), 202

# Signup Routes
@app.route('/signups', methods=['POST'])
def create_signup_route():
    data = request.get_json()
    
    camper_id = data.get('camper_id')
    activity_id = data.get('activity_id')
    time = data.get('time')
    
    if not camper_id or not activity_id:
        return jsonify({"errors": ["camper_id and activity_id are required"]}), 400
    
    result = create_signup(camper_id, activity_id, time)
    
    if isinstance(result, dict) and 'errors' in result:
        return jsonify(result), 400
    
    return jsonify(result), 201

if __name__ == '__main__':
    app.run(debug=True, port=5555)