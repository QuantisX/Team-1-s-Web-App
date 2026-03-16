from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.exc import IntegrityError
from pathlib import Path
from datetime import date


APP_NAME = "Healthy Habits Tracker"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "A Flask web app to track daily healthy habits — sleep, exercise, nutrition, water, and more."

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(app.instance_path) / 'app.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class HabitEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)

    sleep_hours = db.Column(db.Float, default=0)
    sleep_quality = db.Column(db.String(10), default="ok")  # great / ok / bad


    exercise_type = db.Column(db.String(20), default="rest")  # gym, run, walk, yoga, sports, rest
    exercise_minutes = db.Column(db.Integer, default=0)

    meals_count = db.Column(db.Integer, default=3)
    fruit_veggie_servings = db.Column(db.Integer, default=0)
    healthy_food = db.Column(db.Boolean, default=False)

    water = db.Column(db.Integer, default=0)

    gym = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(300), default="")


with app.app_context():
    db.create_all()


@app.get("/")
def home():
    """Home page with app description and quick stats."""
    total_entries = HabitEntry.query.count()

    streak = 0
    today = date.today()
    entries = (
        HabitEntry.query
        .order_by(HabitEntry.date.desc())
        .all()
    )
    if entries:
        from datetime import timedelta
        check_date = today
        entry_dates = {e.date for e in entries}
       
        if today not in entry_dates:
            check_date = today - timedelta(days=1)
        while check_date in entry_dates:
            streak += 1
            check_date -= timedelta(days=1)

    return render_template("index.html", total_entries=total_entries, streak=streak)


@app.route("/log", methods=["GET", "POST"])
def log_habits():
    """Log a new daily habit entry."""
    if request.method == "GET":
        return render_template("add_edit.html", entry=None, editing=False)

   
    date_str = request.form.get("date", "").strip()
    if not date_str:
        flash("Date is required. Please select a date.", "error")
        return redirect(url_for("log_habits"))

  
    try:
        entry_date = date.fromisoformat(date_str)
    except ValueError:
        flash("Invalid date format.", "error")
        return redirect(url_for("log_habits"))

  
    sleep_hours_raw = request.form.get("sleep_hours", "0").strip()
    try:
        sleep_hours = float(sleep_hours_raw) if sleep_hours_raw else 0
    except ValueError:
        sleep_hours = 0
    sleep_quality = request.form.get("sleep_quality", "ok").strip()

    exercise_type = request.form.get("exercise_type", "rest").strip()
    exercise_minutes_raw = request.form.get("exercise_minutes", "0").strip()
    try:
        exercise_minutes = int(exercise_minutes_raw) if exercise_minutes_raw else 0
    except ValueError:
        exercise_minutes = 0


    meals_count_raw = request.form.get("meals_count", "3").strip()
    try:
        meals_count = int(meals_count_raw) if meals_count_raw else 3
    except ValueError:
        meals_count = 3
    fruit_veggie_raw = request.form.get("fruit_veggie_servings", "0").strip()
    try:
        fruit_veggie_servings = int(fruit_veggie_raw) if fruit_veggie_raw else 0
    except ValueError:
        fruit_veggie_servings = 0
    healthy_food = "healthy_food" in request.form

    water_raw = request.form.get("water", "0").strip()
    try:
        water = int(water_raw) if water_raw else 0
    except ValueError:
        water = 0


    gym = "gym" in request.form
    notes = request.form.get("notes", "").strip()

   
    entry = HabitEntry(
        date=entry_date,
        sleep_hours=sleep_hours,
        sleep_quality=sleep_quality,
        exercise_type=exercise_type,
        exercise_minutes=exercise_minutes,
        meals_count=meals_count,
        fruit_veggie_servings=fruit_veggie_servings,
        healthy_food=healthy_food,
        water=water,
        gym=gym,
        notes=notes,
    )

    db.session.add(entry)

    try:
        db.session.commit()
        flash(f"Entry for {entry_date.strftime('%B %d, %Y')} saved successfully!", "success")
        return redirect(url_for("history"))
    except IntegrityError:
        db.session.rollback()
        flash(f"An entry for {entry_date.strftime('%B %d, %Y')} already exists. Please choose another date or edit the existing one.", "warning")
        return redirect(url_for("log_habits"))


@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    """Edit an existing habit entry."""
    entry = HabitEntry.query.get_or_404(entry_id)

    if request.method == "GET":
        return render_template("add_edit.html", entry=entry, editing=True)

  
    sleep_hours_raw = request.form.get("sleep_hours", "0").strip()
    try:
        entry.sleep_hours = float(sleep_hours_raw) if sleep_hours_raw else 0
    except ValueError:
        entry.sleep_hours = 0
    entry.sleep_quality = request.form.get("sleep_quality", "ok").strip()


    entry.exercise_type = request.form.get("exercise_type", "rest").strip()
    exercise_minutes_raw = request.form.get("exercise_minutes", "0").strip()
    try:
        entry.exercise_minutes = int(exercise_minutes_raw) if exercise_minutes_raw else 0
    except ValueError:
        entry.exercise_minutes = 0

    meals_count_raw = request.form.get("meals_count", "3").strip()
    try:
        entry.meals_count = int(meals_count_raw) if meals_count_raw else 3
    except ValueError:
        entry.meals_count = 3
    fruit_veggie_raw = request.form.get("fruit_veggie_servings", "0").strip()
    try:
        entry.fruit_veggie_servings = int(fruit_veggie_raw) if fruit_veggie_raw else 0
    except ValueError:
        entry.fruit_veggie_servings = 0
    entry.healthy_food = "healthy_food" in request.form


    water_raw = request.form.get("water", "0").strip()
    try:
        entry.water = int(water_raw) if water_raw else 0
    except ValueError:
        entry.water = 0


    entry.gym = "gym" in request.form
    entry.notes = request.form.get("notes", "").strip()

    db.session.commit()
    flash(f"Entry for {entry.date.strftime('%B %d, %Y')} updated!", "success")
    return redirect(url_for("history"))


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    """Delete a habit entry."""
    entry = HabitEntry.query.get_or_404(entry_id)
    entry_date = entry.date.strftime("%B %d, %Y")
    db.session.delete(entry)
    db.session.commit()
    flash(f"Entry for {entry_date} deleted.", "success")
    return redirect(url_for("history"))


@app.get("/history")
def history():
    """View all habit entries (newest first)."""
    entries = HabitEntry.query.order_by(HabitEntry.date.desc()).all()
    return render_template("history.html", entries=entries)


@app.get("/detail/<int:entry_id>")
def detail(entry_id):
    """View a single entry in detail."""
    entry = HabitEntry.query.get_or_404(entry_id)
    return render_template("detail.html", entry=entry)


if __name__ == "__main__":
    app.run(debug=True)
