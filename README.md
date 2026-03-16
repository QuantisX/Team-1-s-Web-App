# Healthy Habits Tracker

A Flask web application built as a school group project to help users track daily healthy habits including exercise, sleep, hydration, and nutrition.

---

## Team Members

| Name | Role |
|------|------|
| Quantis | Lead Dev / Repo Manager |
| Elida | Frontend / Full Stack |
| Thaina | Styling (CSS / UX) |
| Anthony | Frontend (HTML) |
| Sesilina | Stats / Evolution |

---

## What the App Does

Users can log daily habits and view their progress over time. The workflow is:

**Log Habits → View History → Check Stats**

### Habits tracked per day

| Category | Fields |
|----------|--------|
| Sleep | Hours slept, quality (great / ok / bad) |
| Exercise | Type (gym, run, walk, yoga, sports, rest — multi-select), duration in minutes |
| Nutrition | Healthy food (yes/no), meals count, fruits & veggies servings |
| Hydration | Water cups |
| Notes | Free text (up to 300 chars) |

### Pages

- **Home** — landing page with app description and navigation
- **Log Habits** — form to log a new daily entry
- **History** — table of all entries with View / Edit / Delete actions
- **Stats** — KPI cards, streaks, Chart.js charts, consistency rings
- **Detail** — full view of a single entry with day score
- **Login / Signup** — simple session-based authentication

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Frontend | HTML, CSS, Jinja2 templates |
| Charts | Chart.js 4.4 (CDN) |
| Auth | Flask sessions (plain text MVP) |
| Version Control | Git + GitHub |

---

## Project Structure

```
Team-1-s-Web-App/
├── healthy_habits_tracker/
│   ├── app.py                  ← Flask routes, models, logic
│   ├── requirements.txt
│   ├── templates/
│   │   ├── base.html           ← shared layout + navbar + flash messages
│   │   ├── home.html           ← landing page
│   │   ├── add_edit.html       ← log + edit form (shared template)
│   │   ├── history.html        ← entry list table
│   │   ├── detail.html         ← single entry detail view
│   │   ├── stats.html          ← charts + streaks + KPIs
│   │   ├── login.html
│   │   └── signup.html
│   ├── static/
│   │   └── style.css
│   └── instance/
│       └── app.db              ← auto-created, do NOT commit
├── .gitignore
└── README.md
```

---

## Prerequisites

- Python 3.10+
- Git
- Internet access (for Google Fonts and Chart.js CDN)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/QuantisX/Team-1-s-Web-App.git
cd Team-1-s-Web-App
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv myproject
myproject\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv myproject
source myproject/bin/activate
```

### 3. Install dependencies

```bash
pip install -r healthy_habits_tracker/requirements.txt
```

### 4. Run the app

**Windows:**
```powershell
flask --app healthy_habits_tracker/app.py run
```

**macOS/Linux:**
```bash
flask --app healthy_habits_tracker/app.py run
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## requirements.txt

```
Flask
Flask-SQLAlchemy
```

To regenerate after installing new packages:
```bash
pip freeze > healthy_habits_tracker/requirements.txt
```

---

## Database

The SQLite database (`app.db`) is created automatically on first run inside the `instance/` folder. No setup needed.

**If you add new model fields**, delete `instance/app.db` and restart Flask — it will recreate the database with the new schema.

> ⚠️ Never commit `app.db` to GitHub. It is listed in `.gitignore`.

---

## Features Implemented

- [x] Home page with hero section and feature cards
- [x] Log Habits form with all habit fields
- [x] Multi-select exercise types (gym, run, walk, yoga, sports, rest)
- [x] History page with sortable table and badges
- [x] Detail page with day score (out of 5)
- [x] Edit and Delete entries
- [x] Flash messages across all pages
- [x] Login and Signup with session management
- [x] Stats page with KPI cards
- [x] Current and best streak tracking (exercise + healthy food)
- [x] Chart.js charts — water bar, sleep line, exercise & food grouped bar
- [x] Doughnut rings — exercise %, clean eating %, hydration goal %
- [x] PRG pattern (Post/Redirect/Get) to prevent duplicate submissions
- [x] Responsive design (mobile-friendly)

---

## Common Issues & Fixes

**"Could not locate a Flask application"**
```bash
flask --app healthy_habits_tracker/app.py run
```

**"python is not recognized" (Windows)**
- Reinstall Python and check **Add Python to PATH**
- Restart terminal

**"no such column" error**
- Delete `healthy_habits_tracker/instance/app.db` and restart Flask

**Port already in use**
```bash
flask --app healthy_habits_tracker/app.py run --port 5001
```

**Charts not rendering**
- Make sure you have internet access (Chart.js loads from CDN)
- Hard refresh: `Ctrl + Shift + R`

---

## Team Workflow (Git)

```bash
# Create a branch for your feature
git checkout -b feature/your-feature-name

# Make changes, then stage and commit
git add .
git commit -m "Brief description of change"

# Push and open a Pull Request
git push origin feature/your-feature-name
```

Review each other's PRs before merging to `main`.

---

## License

MIT License — Copyright (c) 2026 Team 1

