# Healthy Habits Tracker (Flask)

## Overview

**Healthy Habits Tracker** is a Flask web application (school group project) that helps users track daily healthy habits such as:

* Going to the gym
* Drinking water
* Eating healthy food

Users can select a day, submit their habits, and view a list of all submitted days. The project is built with **Python + Flask** and can be extended later with statistics and charts.

---

## What This Group Is For

This project was built by a group to collaborate on planning, development, testing, and documentation.
The group’s purpose is to:

* split responsibilities (backend, frontend, testing, documentation)
* review each other’s code (pull requests, code reviews)
* keep the project organized using issues/tasks
* ensure consistent quality, structure, and deadlines

### Team Members

* **Quantis** 
* **Elida** 
* **Thaina** 
* **Anthony** 
* **Sesilina**

---

## Tech Stack

* Python 3.x
* Flask
* Flask-SQLAlchemy (SQLite database)
* HTML/CSS (Jinja templates)
* Git + GitHub
* (Optional) Chart.js for progress charts

---

## Project Structure

Your repo should look like this (venv is NOT committed to GitHub):

```txt
Team-1-s-Web-App/
├─ healthy_habits_tracker/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ add_edit.html
│  │  └─ detail.html
│  ├─ static/
│  │  └─ style.css
│  └─ instance/
│     └─ app.db   (auto-created)
├─ .gitignore
└─ README.md
```

---

## Prerequisites

* Windows, macOS, or Linux
* Internet access
* Python installed (recommended: Python 3.10+)
* Git installed

---

# Step-by-Step: Install Git

## Windows (Git for Windows)

1. Download Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Run the installer
3. Recommended option: **"Git from the command line and also from 3rd-party software"**
4. Verify:

   ```bash
   git --version
   ```

## macOS

**Option A (recommended): Homebrew**

```bash
brew install git
git --version
```

**Option B: Xcode Command Line Tools**

```bash
xcode-select --install
git --version
```

## Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git -y
git --version
```

---

# Step-by-Step: Clone the Repository

1. Copy the repo URL from GitHub → **Code** → HTTPS
2. Clone and enter the folder:

```bash
git clone https://github.com/QuantisX/Team-1-s-Web-App.git
cd Team-1-s-Web-App
```

Verify:

```bash
git status
git remote -v
```

---

# Step-by-Step: Set Up Python + Flask (Virtual Environment)

## Windows (PowerShell)

From the repo root (`Team-1-s-Web-App/`):

```powershell
# Create venv (do NOT commit this folder)
python -m venv myproject

# Activate venv
myproject\Scripts\Activate.ps1

# Install dependencies
pip install -r healthy_habits_tracker\requirements.txt
```

## macOS/Linux

```bash
python3 -m venv myproject
source myproject/bin/activate
pip install -r healthy_habits_tracker/requirements.txt
```

---

## requirements.txt (example)

Make sure your `healthy_habits_tracker/requirements.txt` includes at least:

```txt
Flask
Flask-SQLAlchemy
```

If you don’t have it yet, you can generate it after installing packages:

```bash
pip freeze > healthy_habits_tracker/requirements.txt
```

---

# Running the Project

## Windows (PowerShell)

From the repo root:

```powershell
myproject\Scripts\Activate.ps1
flask --app healthy_habits_tracker/app.py run
```

## macOS/Linux

```bash
source myproject/bin/activate
flask --app healthy_habits_tracker/app.py run
```

Open in browser:

* [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

# How the Database (instance/app.db) Is Auto-Created

The SQLite database file **`app.db`** is created automatically when:

1. The app config points to SQLite, and
2. The app runs `db.create_all()` to create the tables.

### Minimum example (what app.py should include)

Your `healthy_habits_tracker/app.py` should have logic like this:

* Ensure the instance folder exists
* Configure SQLite
* Create tables at startup

```python
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

# Ensure instance folder exists
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

# This creates the DB inside the instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class HabitEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # add fields here...

with app.app_context():
    db.create_all()
```

After running Flask once, you should see:

```txt
healthy_habits_tracker/instance/app.db
```

---

# Important: Do NOT Push the Virtual Environment to GitHub

Your virtual environment folder (example: `myproject/`) must be ignored.

Create a `.gitignore` in the repo root:

```gitignore
# Virtual environments
myproject/
venv/
.venv/
env/

# Python cache
__pycache__/
*.pyc

# DB files (do not commit local databases)
healthy_habits_tracker/instance/*.db
```

### If you already tracked the venv by mistake

```powershell
git rm -r --cached myproject
git commit -m "Ignore venv folder"
git push
```

---

## Common Issues & Fixes

### “Could not locate a Flask application”

Run Flask with the correct path:

```bash
flask --app healthy_habits_tracker/app.py run
```

### “python is not recognized” (Windows)

* Reinstall Python and check **Add Python to PATH**
* Restart terminal

### “pip not found”

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Port already in use

```bash
flask --app healthy_habits_tracker/app.py run --port 5001
```

---

## Contributing (Team Workflow)

1. Create a branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit changes:

   ```bash
   git add .
   git commit -m "Describe your change"
   ```
3. Push:

   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request on GitHub for review.

---

## License

MIT License (or course-required license)

Copyright (c) 2026
Permission is hereby granted, free of charge, to any person obtaining a copy of this software...
*(keep the standard MIT text if your class allows it)*

