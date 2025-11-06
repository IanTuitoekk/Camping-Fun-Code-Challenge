from flask import request, jsonify
from models import db
from models.camper import Camper

def register_camper_routes(app):
    
    @app.route('/campers', methods=['GET'])
    def get_campers():
        """Get all campers without signups"""
        campers = Camper.query.all()
        return jsonify([camper.to_dict() for camper in campers]), 200

    @app.route('/campers/<int:id>', methods=['GET'])
    def get_camper(id):
        """Get a single camper with signups"""
        camper = Camper.query.get(id)
        if not camper:
            return jsonify({"error": "Camper not found"}), 404
        return jsonify(camper.to_dict(include_signups=True)), 200

    @app.route('/campers', methods=['POST'])
    def create_camper():
        """Create a new camper"""
        data = request.get_json()
        
        try:
            camper = Camper(
                name=data.get('name'),
                age=data.get('age')
            )
            db.session.add(camper)
            db.session.commit()
            return jsonify(camper.to_dict()), 201
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

    @app.route('/campers/<int:id>', methods=['PATCH'])
    def update_camper(id):
        """Update a camper's name and/or age"""
        camper = Camper.query.get(id)
        if not camper:
            return jsonify({"error": "Camper not found"}), 404
        
        data = request.get_json()
        
        try:
            if 'name' in data:
                camper.name = data['name']
            if 'age' in data:
                camper.age = data['age']
            
            db.session.commit()
            return jsonify(camper.to_dict()), 202
        except ValueError as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400