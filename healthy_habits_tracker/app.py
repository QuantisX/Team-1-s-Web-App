from flask import Flask
from flask_sqlalchemy import SQLAlchemy # type: ignore
from pathlib import Path

#  ADDED (needed for graceful duplicate handling)
from sqlalchemy.exc import IntegrityError
from flask import request  # to read form data (POST)

APP_NAME = "Healthy Habits Tracker"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A Flask web app to track daily healthy habits (gym, water, healthy food)."


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"


Path(app.instance_path).mkdir(parents=True, exist_ok=True)


app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(app.instance_path) / 'app.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class HabitEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)  #  already unique
    gym = db.Column(db.Boolean, default=False)
    water = db.Column(db.Integer, default=0)
    healthy_food = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(300), default="")

 
with app.app_context():
    db.create_all()

@app.get("/")
def home():
    return "Flask is running! DB ready! Check the instance/app.db file."


@app.route("/log", methods=["GET", "POST"])
def log_habits():
    if request.method == "GET":
        
        return """
        <h1>Log Habits</h1>
        <form method="POST">
            <label>Date:</label>
            <input type="date" name="date" required><br><br>

            <label>Gym:</label>
            <input type="checkbox" name="gym"><br><br>

            <label>Water (cups):</label>
            <input type="number" name="water" min="0" value="0"><br><br>

            <label>Healthy Food:</label>
            <input type="checkbox" name="healthy_food"><br><br>

            <label>Notes:</label><br>
            <textarea name="notes" maxlength="300"></textarea><br><br>

            <button type="submit">Save</button>
        </form>
        <p><a href="/">Back home</a></p>
        """

    
    date_str = request.form.get("date", "").strip()
    if not date_str:
        return "Date is required. Please go back and select a date.", 400

   
    gym = "gym" in request.form
    healthy_food = "healthy_food" in request.form

    
    water_raw = request.form.get("water", "0").strip()
    try:
        water = int(water_raw) if water_raw else 0
    except ValueError:
        water = 0

    notes = request.form.get("notes", "").strip()

   
    entry = HabitEntry(
        date=date_str, 
        gym=gym,
        water=water,
        healthy_food=healthy_food,
        notes=notes
    )

    db.session.add(entry)

   
    try:
        db.session.commit()
        return f"Saved entry for {date_str}! ✅ <br><a href='/log'>Log another</a>"
    except IntegrityError:
        db.session.rollback()
        return (
            f"⚠️ An entry for <b>{date_str}</b> already exists. "
            f"Please choose another date or edit the existing one. "
            f"<br><a href='/log'>Back to form</a>"
        ), 409


if __name__ == "__main__":
    app.run(debug=True)
