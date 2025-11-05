from flask import Flask
from models import db
from server.config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Import models so Flask-Migrate can detect them
from models.camper import Camper
from models.activity import Activity
from models.signup import Signup

if __name__ == '__main__':
    app.run(port=5555, debug=True)