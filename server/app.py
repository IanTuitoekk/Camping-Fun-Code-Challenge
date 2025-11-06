from flask import Flask
from models import db
from server.config import Config
from flask_migrate import Migrate

# Import route registration functions
from controllers.camper_controller import register_camper_routes
from controllers.activity_controller import register_activity_routes
from controllers.signup_controller import register_signup_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Import models for Flask-Migrate
from models.camper import Camper
from models.activity import Activity
from models.signup import Signup

# Register routes
register_camper_routes(app)
register_activity_routes(app)
register_signup_routes(app)

@app.route('/')
def home():
    return {"message": "Welcome to Camping API with PostgreSQL"}, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)