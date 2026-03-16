from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.exc import IntegrityError
from pathlib import Path
from datetime import datetime

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

@app.route("/")
def home():
    total_entries = HabitEntry.query.count()
    entries = HabitEntry.query.order_by(HabitEntry.date.desc()).all()

    streak = 0
    if entries:
        from datetime import timedelta

        today = datetime.today().date()
        check_date = today
        entry_dates = {e.date for e in entries}

        if today not in entry_dates:
            check_date = today - timedelta(days=1)

        while check_date in entry_dates:
            streak += 1
            check_date -= timedelta(days=1)

    return render_template(
        "index.html",
        total_entries=total_entries,
        streak=streak,
        entries=entries,
    )


@app.route("/add", methods=["GET", "POST"], endpoint="add_entry")
@app.route("/log", methods=["GET", "POST"])
def log_habits():
    if request.method == "GET":
        return render_template(
            "add_edit.html",
            entry=None,
            editing=False,
            page_title="Add Entry",
        )

    date_str = request.form.get("date", "").strip()
    if not date_str:
        flash("Date is required.", "error")
        return redirect(url_for("log_habits"))

    try:
        entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.", "error")
        return redirect(url_for("log_habits"))

    def parse_int(name: str, default: int = 0) -> int:
        raw = request.form.get(name, str(default)).strip()
        try:
            return int(raw) if raw else default
        except ValueError:
            return default

    def parse_float(name: str, default: float = 0.0) -> float:
        raw = request.form.get(name, str(default)).strip()
        try:
            return float(raw) if raw else default
        except ValueError:
            return default

    sleep_hours = parse_float("sleep_hours", 0.0)
    sleep_quality = request.form.get("sleep_quality", "ok").strip()
    exercise_type = request.form.get("exercise_type", "rest").strip()
    exercise_minutes = parse_int("exercise_minutes", 0)
    meals_count = parse_int("meals_count", 3)
    fruit_veggie_servings = parse_int("fruit_veggie_servings", 0)
    healthy_food = "healthy_food" in request.form
    water = parse_int("water", 0)
    gym = "gym" in request.form
    notes = request.form.get("notes", "").strip()

    entry = HabitEntry(
        date=entry_date,
        healthy_food=healthy_food,
        water=water,
        gym=gym,
        notes=notes,
    )

    optional_fields = {
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "exercise_type": exercise_type,
        "exercise_minutes": exercise_minutes,
        "meals_count": meals_count,
        "fruit_veggie_servings": fruit_veggie_servings,
    }
    for field, value in optional_fields.items():
        if hasattr(entry, field):
            setattr(entry, field, value)

    db.session.add(entry)
    try:
        db.session.commit()
        flash("Entry added successfully.", "success")
        return redirect(url_for("history"))
    except IntegrityError:
        db.session.rollback()
        flash("An entry for that date already exists.", "error")
        return redirect(url_for("log_habits"))
    except Exception:
        db.session.rollback()
        flash("Something went wrong while adding the entry.", "error")
        return redirect(url_for("log_habits"))


@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)

    if request.method == "GET":
        return render_template(
            "add_edit.html",
            entry=entry,
            editing=True,
            page_title="Edit Entry",
        )

    date_str = request.form.get("date", "").strip()
    if not date_str:
        flash("Date is required.", "error")
        return redirect(url_for("edit_entry", entry_id=entry_id))

    try:
        entry.date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.", "error")
        return redirect(url_for("edit_entry", entry_id=entry_id))

    def parse_int(name: str, default: int = 0) -> int:
        raw = request.form.get(name, str(default)).strip()
        try:
            return int(raw) if raw else default
        except ValueError:
            return default

    def parse_float(name: str, default: float = 0.0) -> float:
        raw = request.form.get(name, str(default)).strip()
        try:
            return float(raw) if raw else default
        except ValueError:
            return default

    entry.gym = "gym" in request.form
    entry.healthy_food = "healthy_food" in request.form
    entry.water = parse_int("water", 0)
    entry.notes = request.form.get("notes", "").strip()

    optional_fields = {
        "sleep_hours": parse_float("sleep_hours", 0.0),
        "sleep_quality": request.form.get("sleep_quality", "ok").strip(),
        "exercise_type": request.form.get("exercise_type", "rest").strip(),
        "exercise_minutes": parse_int("exercise_minutes", 0),
        "meals_count": parse_int("meals_count", 3),
        "fruit_veggie_servings": parse_int("fruit_veggie_servings", 0),
    }
    for field, value in optional_fields.items():
        if hasattr(entry, field):
            setattr(entry, field, value)

    try:
        db.session.commit()
        flash("Entry updated successfully.", "success")
        return redirect(url_for("history"))
    except IntegrityError:
        db.session.rollback()
        flash("Another entry already uses that date.", "error")
        return redirect(url_for("edit_entry", entry_id=entry_id))
    except Exception:
        db.session.rollback()
        flash("Something went wrong while updating the entry.", "error")
        return redirect(url_for("edit_entry", entry_id=entry_id))


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)

    try:
        db.session.delete(entry)
        db.session.commit()
        flash("Entry deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Could not delete the entry.", "error")

    return redirect(url_for("history"))


@app.get("/history")
def history():
    entries = HabitEntry.query.order_by(HabitEntry.date.desc()).all()
    return render_template("history.html", entries=entries)


@app.route("/entry/<int:entry_id>", endpoint="entry_detail")
@app.get("/detail/<int:entry_id>")
def detail(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)
    return render_template("detail.html", entry=entry)

if __name__ == "__main__":
    app.run(debug=True)
