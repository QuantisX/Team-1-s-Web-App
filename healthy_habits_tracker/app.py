from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.exc import IntegrityError
from pathlib import Path
from datetime import date as date_type, timedelta
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-in-production"

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(app.instance_path) / 'app.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class HabitEntry(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    date         = db.Column(db.Date, unique=True, nullable=False)

    # original fields
    gym          = db.Column(db.Boolean, default=False)
    water        = db.Column(db.Integer, default=0)
    healthy_food = db.Column(db.Boolean, default=False)
    notes        = db.Column(db.String(300), default="")

    # sleep
    sleep_hours   = db.Column(db.Float,      default=0.0)
    sleep_quality = db.Column(db.String(10), default="ok")   

    # exercise
    exercise_type     = db.Column(db.String(20), default="none")  
    exercise_duration = db.Column(db.Integer,    default=0)     

    # nutrition
    meals_count = db.Column(db.Integer, default=0)
    fruits_veg  = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()



def safe_int(val, fallback=0):
    try:
        return int(val) if val else fallback
    except (ValueError, TypeError):
        return fallback


def safe_float(val, fallback=0.0):
    try:
        return float(val) if val else fallback
    except (ValueError, TypeError):
        return fallback


def compute_streak(entries, field):
    """Count current consecutive days streak (most recent first)."""
    streak   = 0
    today    = date_type.today()
    sorted_e = sorted(entries, key=lambda e: e.date, reverse=True)
    expected = today
    for e in sorted_e:
        if e.date > expected:
            continue
        if e.date < expected - timedelta(days=1):
            break
        if getattr(e, field):
            streak  += 1
            expected = e.date - timedelta(days=1)
        else:
            break
    return streak


def compute_best_streak(entries, field):
    """Find the longest ever consecutive streak for a field."""
    sorted_e = sorted(entries, key=lambda e: e.date)
    best = current = 0
    prev_date = None
    for e in sorted_e:
        if getattr(e, field):
            if prev_date and (e.date - prev_date).days == 1:
                current += 1
            else:
                current = 1
            best = max(best, current)
        else:
            current = 0
        prev_date = e.date
    return best


def _did_exercise(entry):
    """True if the entry has any exercise (not none/rest/empty)."""
    t = (entry.exercise_type or '').lower()
    return bool(t) and t not in ('none', 'rest', '')


def compute_exercise_streak(entries):
    """Current consecutive days with any exercise."""
    streak   = 0
    today    = date_type.today()
    sorted_e = sorted(entries, key=lambda e: e.date, reverse=True)
    expected = today
    for e in sorted_e:
        if e.date > expected:
            continue
        if e.date < expected - timedelta(days=1):
            break
        if _did_exercise(e):
            streak  += 1
            expected = e.date - timedelta(days=1)
        else:
            break
    return streak


def compute_best_exercise_streak(entries):
    """Best ever consecutive exercise streak."""
    sorted_e = sorted(entries, key=lambda e: e.date)
    best = current = 0
    prev_date = None
    for e in sorted_e:
        if _did_exercise(e):
            if prev_date and (e.date - prev_date).days == 1:
                current += 1
            else:
                current = 1
            best = max(best, current)
        else:
            current = 0
        prev_date = e.date
    return best



def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated



@app.get("/")
def home():
    return render_template("home.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user"):
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm",  "").strip()
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("signup.html")
        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html")
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("signup.html")
        db.session.add(User(username=username, password=password))
        db.session.commit()
        session["user"] = username
        flash(f"Welcome, {username}! Account created.", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user     = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")



@app.get("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))



@app.get("/history")
@login_required
def index():
    entries = HabitEntry.query.order_by(HabitEntry.date.desc()).all()
    return render_template("history.html", entries=entries)



@app.route("/log", methods=["GET", "POST"])
@login_required
def add_entry():
    if request.method == "POST":
        date_str = request.form.get("date", "").strip()
        if not date_str:
            flash("Date is required.", "error")
            return render_template("add_edit.html", entry=None)
        try:
            parsed_date = date_type.fromisoformat(date_str)
        except ValueError:
            flash("Invalid date format.", "error")
            return render_template("add_edit.html", entry=None)

        ex_types = [t for t in request.form.getlist('exercise_types') if t]
        ex_str   = ','.join(ex_types) if ex_types else 'none'
        entry = HabitEntry(
            date              = parsed_date,
            gym               = 'gym' in ex_types,
            water             = safe_int(request.form.get("water")),
            healthy_food      = "healthy_food" in request.form,
            notes             = request.form.get("notes", "").strip(),
            sleep_hours       = safe_float(request.form.get("sleep_hours")),
            sleep_quality     = request.form.get("sleep_quality", "ok"),
            exercise_type     = ex_str,
            exercise_duration = safe_int(request.form.get("exercise_duration")),
            meals_count       = safe_int(request.form.get("meals_count")),
            fruits_veg        = safe_int(request.form.get("fruits_veg")),
        )
        db.session.add(entry)
        try:
            db.session.commit()
            flash(f"Entry for {parsed_date} saved! Keep it up!", "success")
            return redirect(url_for("index"))
        except IntegrityError:
            db.session.rollback()
            flash(f"Entry for {parsed_date} already exists. Edit it instead.", "error")
            return render_template("add_edit.html", entry=None)

    return render_template("add_edit.html", entry=None)



@app.route("/log/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)
    if request.method == "POST":
        ex_types = [t for t in request.form.getlist('exercise_types') if t]
        ex_str   = ','.join(ex_types) if ex_types else 'none'
        entry.gym               = 'gym' in ex_types
        entry.water             = safe_int(request.form.get("water"))
        entry.healthy_food      = "healthy_food" in request.form
        entry.notes             = request.form.get("notes", "").strip()
        entry.sleep_hours       = safe_float(request.form.get("sleep_hours"))
        entry.sleep_quality     = request.form.get("sleep_quality", "ok")
        entry.exercise_type     = ex_str
        entry.exercise_duration = safe_int(request.form.get("exercise_duration"))
        entry.meals_count       = safe_int(request.form.get("meals_count"))
        entry.fruits_veg        = safe_int(request.form.get("fruits_veg"))
        db.session.commit()
        flash("Entry updated successfully!", "success")
        return redirect(url_for("detail", entry_id=entry.id))
    return render_template("add_edit.html", entry=entry)



@app.post("/log/<int:entry_id>/delete")
@login_required
def delete_entry(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "info")
    return redirect(url_for("index"))



@app.get("/log/<int:entry_id>")
@login_required
def detail(entry_id):
    entry = HabitEntry.query.get_or_404(entry_id)
    return render_template("detail.html", entry=entry)



@app.get("/stats")
@login_required
def get_stats():
    entries = HabitEntry.query.order_by(HabitEntry.date.asc()).all()
    total   = len(entries)

    empty_stats = dict(
        total_days=0, exercise_count=0, exercise_pct=0,
        avg_water=0, avg_sleep=0, healthy_count=0, healthy_pct=0,
        water_goal_pct=0, exercise_streak=0, exercise_best_streak=0,
        food_streak=0, food_best_streak=0,
        avg_exercise_min=0, avg_fruits_veg=0,
    )
    if total == 0:
        return render_template("stats.html", stats=empty_stats,
                               chart_labels=[], chart_water=[],
                               chart_exercise=[], chart_food=[], chart_sleep=[])

    exercise_count = sum(1 for e in entries if _did_exercise(e))
    healthy_count  = sum(1 for e in entries if e.healthy_food)
    avg_water      = round(sum(e.water for e in entries) / total, 1)
    avg_sleep      = round(sum(e.sleep_hours for e in entries) / total, 1)
    avg_ex_min     = round(sum(e.exercise_duration for e in entries) / total, 1)
    avg_fv         = round(sum(e.fruits_veg for e in entries) / total, 1)
    water_goal     = round(sum(1 for e in entries if e.water >= 8) / total * 100)

    stats = dict(
        total_days           = total,
        exercise_count       = exercise_count,
        exercise_pct         = round(exercise_count / total * 100),
        avg_water            = avg_water,
        avg_sleep            = avg_sleep,
        healthy_count        = healthy_count,
        healthy_pct          = round(healthy_count / total * 100),
        water_goal_pct       = water_goal,
        exercise_streak      = compute_exercise_streak(entries),
        exercise_best_streak = compute_best_exercise_streak(entries),
        food_streak          = compute_streak(entries, "healthy_food"),
        food_best_streak     = compute_best_streak(entries, "healthy_food"),
        avg_exercise_min     = avg_ex_min,
        avg_fruits_veg       = avg_fv,
    )

    last3         = entries[-7:]
    chart_labels  = [e.date.strftime("%b %d") for e in last3]
    chart_water   = [e.water for e in last3]
    chart_exercise= [1 if _did_exercise(e) else 0 for e in last3]
    chart_food    = [1 if e.healthy_food else 0 for e in last3]
    chart_sleep   = [e.sleep_hours for e in last3]

    return render_template("stats.html",
                           stats=stats,
                           chart_labels=chart_labels,
                           chart_water=chart_water,
                           chart_exercise=chart_exercise,
                           chart_food=chart_food,
                           chart_sleep=chart_sleep)



if __name__ == "__main__":
    app.run(debug=True)
