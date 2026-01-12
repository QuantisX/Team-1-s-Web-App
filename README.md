
# [Project Name]

## Overview
[Project Name WE NEED DECIDE] is a [short description: e.g., Flask web app / API / school project] created to [main goal: e.g., manage tasks, analyze data, provide an endpoint, etc.].  
This repository contains the source code, setup instructions, and documentation needed to run the project locally.

---

## What This Group Is For
This project was built by a group to collaborate on planning, development, testing, and documentation.  
The group’s purpose is to:
- split responsibilities (backend, frontend, testing, documentation)
- review each other’s code (pull requests, code reviews)
- keep the project organized using issues/tasks
- ensure consistent quality, structure, and deadlines

**Team Members**
- Quantis — [Role: e.g., Backend / API / Database]??
- Elida— [Role: e.g., Frontend / UI]??
- Thaina — [Role: e.g., Testing / Documentation]??
- Anthony — [Role: e.g., Project Manager / Integration]??

---

## Tech Stack
- Python
- Flask
- Git + GitHub
- [Optional: SQLite/PostgreSQL, HTML/CSS, React, etc.]

---

## Prerequisites
- A computer with Windows, macOS, or Linux
- Internet access
- Admin permissions to install software

---

# Step-by-Step: Install Git

## Windows (Git for Windows)
1. Download Git from the official website: https://git-scm.com/downloads
2. Run the installer.
3. Recommended options during install:
   - Keep default settings (safe choice)
   - Choose **"Git from the command line and also from 3rd-party software"**
4. After installation, open **PowerShell** or **Command Prompt** and verify:
   ```bash
   git --version
````

## macOS

**Option A (recommended): Homebrew**

1. Install Homebrew (if needed): [https://brew.sh/](https://brew.sh/)
2. Install Git:

   ```bash
   brew install git
   ```
3. Verify:

   ```bash
   git --version
   ```

**Option B:** Install Xcode Command Line Tools

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

# Step-by-Step: Clone a GitHub Repository

## 1) Copy the Repo URL

On GitHub:

1. Open the repository page
2. Click **Code**
3. Copy the **HTTPS** URL (easy) or **SSH** URL (advanced)

## 2) Clone in your Terminal

Go to the folder where you want the project:

```bash
cd path/to/your/folder
```

Clone the repository:

```bash
git clone https://github.com/QuantisX/Team-1-s-Web-App.git
```

Enter the project folder:

```bash
cd Team-1-s-Web-App
```

Verify:

```bash
git status
git remote -v
```

---

# Steps to Install Flask



**Step 1: Install Python**

Ensure Python is installed on your system. Download the latest version from the official Python website if not already installed.

During installation, check the box to Add Python to PATH.

**Step 2: Install virtualenv**

Open a terminal or command prompt.

Run the command: pip install virtualenv.

**Step 3: Create a Virtual Environment**

Navigate to the directory where you want to create your project.

Run the following command: On Windows: python -m venv myproject On macOS/Linux: python3 -m venv myproject

Replace myproject with your desired virtual environment name.

**Step 4: Activate the Virtual Environment**

Activate the environment: On Windows: myproject\Scripts\activate On macOS/Linux: source myproject/bin/activate

The terminal prompt will change to indicate the virtual environment is active.

**Step 5: Install Flask**

With the virtual environment activated, run the command: pip install Flask.

**Step 6: Verify Installation**

Run the command: python -m flask --version.

If Flask's version is displayed, the installation is successful.

---

## Running the Project (Example)

> Update these commands to match your project structure.

### Windows (PowerShell)

```bash
# inside your repo folder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# set Flask app (example)
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### macOS/Linux

```bash
# inside your repo folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# set Flask app (example)
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Open in your browser:

* [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Project Structure (Example)

```txt
[Project Name]/
├─ app.py
├─ requirements.txt
├─ README.md
├─ templates/
├─ static/
└─ ...
```

---

## Common Issues & Fixes

### "python is not recognized" (Windows)

* Reinstall Python and check **Add Python to PATH**
* Close and reopen the terminal

### "pip not found"

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Port already in use

Run Flask on another port:

```bash
flask run --port 5001
```

---

## Contributing (Team Workflow)

1. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make changes and commit:

   ```bash
   git add .
   git commit -m "Describe your change"
   ```
3. Push branch:

   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request on GitHub for review.

---

## License

Copyright (c) 2026 [Full Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
