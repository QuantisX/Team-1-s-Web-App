## Healthy Habits Tracker (Flask)

Overview

Healthy Habits Tracker is a Flask web application (school group project) that helps users track daily healthy habits such as:

Going to the gym
Drinking water
Eating healthy food

Users can select a day, submit their habits, and view a list of all submitted days. The project is built with Python + Flask and can be extended later with statistics and charts.

---

## MVP Description (5–10 sentences)

Healthy Habits Tracker solves the problem of forgetting or inconsistently tracking daily healthy habits. It is designed for students and busy individuals who want a simple way to record healthy behaviors without complex features. The app allows a user to choose a date and log whether they went to the gym, how much water they drank, and whether they ate healthy food that day. The user can submit the entry and then view a history of previous days they recorded. The MVP focuses on creating a useful daily log with a clear, repeatable workflow: select date → record habits → submit → view history. The app is intentionally lightweight so it can be built quickly and used immediately. Future versions may add charts or statistics, but the MVP is mainly about saving and viewing daily habit records.

---

## Scope (MVP)

The MVP will include only the core features needed for a basic habit-tracking productivity app:

* A Home page that explains what the app does and provides navigation.
* A Log Habits page where the user selects a date and submits habit data (gym, water, healthy food).
* A History page that displays all saved entries in a readable list.
* Basic validation and friendly error messages (example: date is required).
* Simple storage for entries (in-memory for Sprint 3), with the option to add a database later.

---

## Objectives (Sprint 3)

In Sprint 3, the team aims to complete a working MVP that can be run locally by any team member:

* Implement Flask routes for Home, Log (GET/POST), and History.
* Build basic HTML templates using a shared base layout with navigation.
* Implement a simple storage method to save and retrieve habit entries.
* Use Post/Redirect/Get after form submission to prevent duplicate submits on refresh.
* Display saved entries clearly in History (date + habit values).
* Ensure the app runs consistently for the team using `requirements.txt` and README setup steps.

---

## Requirements

### Functional Requirements

1. The app must display a Home page with a short description of the project and navigation links.
2. The app must allow the user to open a Log Habits page and submit a habit entry for a selected date.
3. The Log Habits form must include at least these habit fields: gym (yes/no), water (number), healthy food (yes/no).
4. The app must validate that the date field is required and show a friendly error message if missing.
5. The app must save submitted habit entries using a consistent storage method (MVP storage can be in-memory).
6. The app must provide a History page that lists all submitted habit entries.
7. After a successful form submission, the app must redirect to another page (PRG pattern) to avoid duplicate form submission on refresh.
8. The app should allow viewing entries even when no entries exist (show “No entries yet” message).

### Non-Functional Requirements

1. The application must be built using Python + Flask.
2. The project must run locally on Windows/macOS/Linux using the instructions in the README.
3. The project must include a `requirements.txt` so dependencies install consistently.
4. The project must not require login/authentication for the MVP.
5. The MVP should remain simple (no advanced features required like charts, accounts, or cloud hosting).
6. The code must be organized with a clear folder structure (`templates/`, `static/`, `app.py`).
7. The repository must use GitHub issues and a Kanban board to track tasks and progress.

---

## User Stories (5–8)

1. As a user, I want to open the app and understand what it does so I know how to use it.
2. As a user, I want to select a date and log my habits so I can record what I did that day.
3. As a user, I want to submit my habit entry and receive confirmation so I know it saved successfully.
4. As a user, I want to see a history of my entries so I can review my past habit tracking.
5. As a user, I want the app to warn me if I forget to select a date so I can fix the form and submit correctly.
6. As a user, I want the app to handle an empty history page nicely so I don’t get confused when I have no entries yet.
7. As a developer on the team, I want clear setup instructions so I can run the project without troubleshooting.
8. As a team member, I want tasks split into issues so we can work in parallel and review each other’s work.

---

What This Group Is For
This project was built by a group to collaborate on planning, development, testing, and documentation. The group’s purpose is to:

split responsibilities (backend, frontend, testing, documentation)
review each other’s code (pull requests, code reviews)
keep the project organized using issues/tasks
ensure consistent quality, structure, and deadlines

Team Members
Quantis
Elida
Thaina
Anthony
Sesilina

Tech Stack
Python 3.x
Flask
Flask-SQLAlchemy (SQLite database)
HTML/CSS (Jinja templates)
Git + GitHub
(Optional) Chart.js for progress charts

---

## Project Structure

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
Prerequisites
Windows, macOS, or Linux
Internet access
Python installed (recommended: Python 3.10+)
Git installed

Step-by-Step: Install Git
Windows (Git for Windows)
Download Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)

Run the installer

Recommended option: "Git from the command line and also from 3rd-party software"

Verify:

git --version

macOS
Option A (recommended): Homebrew

brew install git
git --version

Option B: Xcode Command Line Tools

xcode-select --install
git --version

Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git -y
git --version

Step-by-Step: Clone the Repository
Copy the repo URL from GitHub → Code → HTTPS
Clone and enter the folder:
git clone [https://github.com/QuantisX/Team-1-s-Web-App.git](https://github.com/QuantisX/Team-1-s-Web-App.git)
cd Team-1-s-Web-App

Verify:

git status
git remote -v

Step-by-Step: Set Up Python + Flask (Virtual Environment)
Windows (PowerShell)
From the repo root (Team-1-s-Web-App/):

# Create venv (do NOT commit this folder)

python -m venv myproject

# Activate venv

myproject\Scripts\Activate.ps1

# Install dependencies

pip install -r healthy_habits_tracker\requirements.txt

macOS/Linux
python3 -m venv myproject
source myproject/bin/activate
pip install -r healthy_habits_tracker/requirements.txt

requirements.txt (example)
Make sure your healthy_habits_tracker/requirements.txt includes at least:

Flask
Flask-SQLAlchemy

If you don’t have it yet, you can generate it after installing packages:

pip freeze > healthy_habits_tracker/requirements.txt

Running the Project
Windows (PowerShell)
From the repo root:

myproject\Scripts\Activate.ps1
flask --app healthy_habits_tracker/app.py run

macOS/Linux
source myproject/bin/activate
flask --app healthy_habits_tracker/app.py run

Open in browser:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

How the Database (instance/app.db) Is Auto-Created
The SQLite database file app.db is created automatically when:

The app config points to SQLite, and
The app runs db.create_all() to create the tables.

Minimum example (what app.py should include)
Your healthy_habits_tracker/app.py should have logic like this:

Ensure the instance folder exists
Configure SQLite
Create tables at startup

from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(**name**)
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

After running Flask once, you should see:

healthy_habits_tracker/instance/app.db

Important: Do NOT Push the Virtual Environment to GitHub
Your virtual environment folder (example: myproject/) must be ignored.

Create a .gitignore in the repo root:

# Virtual environments

myproject/
venv/
.venv/
env/

# Python cache

**pycache**/
*.pyc

# DB files (do not commit local databases)

healthy_habits_tracker/instance/*.db

If you already tracked the venv by mistake
git rm -r --cached myproject
git commit -m "Ignore venv folder"
git push

Common Issues & Fixes
“Could not locate a Flask application”
Run Flask with the correct path:

flask --app healthy_habits_tracker/app.py run

“python is not recognized” (Windows)
Reinstall Python and check Add Python to PATH
Restart terminal

“pip not found”
python -m ensurepip --upgrade
python -m pip install --upgrade pip

Port already in use
flask --app healthy_habits_tracker/app.py run --port 5001

Contributing (Team Workflow)
Create a branch:

git checkout -b feature/your-feature-name

Commit changes:

git add .
git commit -m "Describe your change"

Push:

git push origin feature/your-feature-name

Open a Pull Request on GitHub for review.

License
MIT License (or course-required license)

Copyright (c) 2026 Permission is hereby granted, free of charge, to any person obtaining a copy of this software... (keep the standard MIT text if your class allows it)
