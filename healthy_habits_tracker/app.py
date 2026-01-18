from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

APP_NAME = "Healthy Habits Tracker"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A Flask web app to track daily healthy habits (gym, water, healthy food)."


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"


Path(app.instance_path).mkdir(parents=True, exist_ok=True)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class HabitEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    gym = db.Column(db.Boolean, default=False)
    water = db.Column(db.Integer, default=0)
    healthy_food = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(300), default="")

 
with app.app_context():
    db.create_all()

@app.get("/")
def home():
    return "DB ready! Check the instance/app.db file."
