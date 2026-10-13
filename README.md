# DrugReminder

DrugReminder is a hospital medication-management and care-coordination web application built with Python, Flask, Supabase and PostgreSQL.

The project is being designed for hospitals that need a structured way to manage branches, departments, staff, patients and medication activities while keeping each hospital's data separate and secure.

> **Project status:** Active development. The hospital/staff foundation is being built first. Patient management and the complete medication reminder, confirmation, missed-task and escalation workflows are still under development.

## Table of Contents

- [What DrugReminder Does](#what-drugreminder-does)
- [Main Goals](#main-goals)
- [Current Features](#current-features)
- [Planned Features](#planned-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [How to Run the Application](#how-to-run-the-application)
- [Basic Application Flow](#basic-application-flow)
- [Database and Supabase](#database-and-supabase)
- [Security](#security)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Project Documentation](#project-documentation)

## What DrugReminder Does

DrugReminder is intended to help hospitals organize medication-related responsibilities and follow-up.

The finished workflow is intended to answer important questions such as:

- Which patient needs medication?
- What medication should be administered?
- When should it be administered?
- Which nurse or caregiver is responsible?
- Was the medication confirmed as administered?
- What happens if the task is missed or not confirmed?
- Who should be notified or assigned next?

DrugReminder is a multi-hospital system. A hospital may have several branches, but a completely different hospital remains a separate organization and should not have access to another hospital's private information.

## Main Goals

The project aims to provide:

- hospital and branch management;
- department management;
- staff management and assignment history;
- patient management;
- medication scheduling;
- medication reminders and alerts;
- administration confirmation;
- missed/not-confirmed task handling;
- nurse reassignment and escalation;
- doctor and nurse workflows;
- audit/history records;
- secure separation of hospital data.

## Current Features

The project currently includes or has begun implementing:

- Flask web application;
- Supabase authentication integration;
- hospital registration;
- hospital branch registration;
- department registration;
- hospital membership handling;
- staff registration;
- staff assignment records;
- hospital staff listing;
- duplicate Staff ID protection;
- live validation on the staff registration form;
- PostgreSQL/Supabase data storage;
- Row Level Security policies for hospital data isolation.

## Planned Features

Major features still being developed include:

- complete staff transfer/history workflow;
- patient registration and management;
- doctor-to-patient relationships;
- medication and dosage management;
- medication scheduling;
- five-minute pre-notifications;
- scheduled-time medication alerts;
- nurse administration confirmation;
- missed/not-confirmed medication tracking;
- reason capture;
- doctor/Head Nurse escalation;
- automatic nurse reassignment based on availability, workload and location;
- authorized rescheduling while preserving the original missed record;
- patient emergency and normal/home-delivery requests;
- role-specific dashboards;
- complete audit trail;
- production-ready user interface;
- automated testing and deployment.

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Main backend programming language |
| Flask | Web application framework |
| Supabase | Authentication and database platform |
| PostgreSQL | Relational database |
| HTML | Page and form structure |
| CSS | User-interface styling |
| JavaScript | Browser-side behavior and live validation |
| Git | Source-control/version history |
| GitHub | Remote repository and project backup/collaboration |

## Project Structure

The structure will continue to grow as new features are implemented.

```text
DrugReminder/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env                 # local only; never commit secrets
├── docs/
│   └── DRUGREMINDER_PROJECT_LEARNING_GUIDE.md
└── templates/
    ├── dashboard.html
    ├── login.html
    ├── signup.html
    ├── register_hospital.html
    ├── register_branch.html
    ├── register_department.html
    ├── register_staff.html
    └── staff_list.html
```

### Important files

**`app.py`** — Main Flask application. It contains routes that receive browser requests, process forms, call database functions and render/redirect pages.

**`database.py`** — Contains functions used by the Flask application to communicate with Supabase.

**`templates/`** — Contains the HTML templates rendered by Flask.

**`requirements.txt`** — Lists the Python packages required to run the application.

**`.env`** — Stores local environment variables and secrets. This file must not be pushed to GitHub.

**`.gitignore`** — Tells Git which local/generated/sensitive files should not be tracked.

**`docs/DRUGREMINDER_PROJECT_LEARNING_GUIDE.md`** — Detailed beginner-friendly project explanation, design decisions, challenges, lessons and file explanations. It is different from this README.

## Requirements

Before running the project locally, install:

- Python 3;
- Git;
- a code editor such as VS Code;
- access to the configured Supabase project (for database/authentication functionality).

On Ubuntu/Linux, check Python and Git with:

```bash
python3 --version
git --version
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ejembiedwin36-oss/DrugReminder.git
cd DrugReminder
```

If the repository is already on your computer, do not clone it again. Open the existing `DrugReminder` folder instead.

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Linux/macOS:

```bash
source venv/bin/activate
```

When it is active, the terminal normally shows `(venv)` near the prompt.

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

The project currently depends on Flask and the Supabase Python client. Their version ranges are defined in `requirements.txt`.

## Environment Variables

Create a file named `.env` in the project root.

Do **not** commit `.env` to GitHub and do not share its secret values publicly.

The application currently expects these variables:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_or_anon_key
FLASK_SECRET_KEY=your_private_random_flask_secret
```

### What they mean

`SUPABASE_URL` tells the application which Supabase project to connect to.

`SUPABASE_KEY` is the client key used by the application to communicate with Supabase. Use the appropriate project client/publishable/anon key for the current setup; do not place privileged server secrets in browser code or documentation.

`FLASK_SECRET_KEY` is used by Flask to protect session data. Use a private, unpredictable value in real deployments.

## How to Run the Application

Make sure you are inside the `DrugReminder` directory and the virtual environment is active.

Run:

```bash
python3 app.py
```

Flask should start the development server. The terminal will display the local address. With the current development setup this is normally:

```text
http://127.0.0.1:5000
```

Open that address in a browser.

To stop the development server, return to the terminal and press:

```text
Ctrl + C
```

### Starting the project again later

You normally only need:

```bash
cd DrugReminder
source venv/bin/activate
python3 app.py
```

You do not recreate the virtual environment every time.

## Basic Application Flow

A simple way to understand the application is:

```text
Browser
   ↓
HTML form/template
   ↓
Flask route (app.py)
   ↓
Database helper (database.py)
   ↓
Supabase / PostgreSQL
   ↓
Result returns to Flask
   ↓
Flask renders or redirects to a page
```

For example, staff registration follows this general flow:

```text
Register Staff page
        ↓
User fills the form
        ↓
Live JavaScript validation
        ↓
Form submitted to Flask
        ↓
app.py reads the values
        ↓
database.py sends data to Supabase
        ↓
PostgreSQL checks security/constraints
        ↓
Staff is stored
        ↓
Staff assignment is created
        ↓
User is redirected to the Staff List
```

## Database and Supabase

The current database design includes these main concepts:

- `hospitals`
- `hospital_branches`
- `departments`
- `hospital_users`
- `staff`
- `staff_assignments`

The schema will grow as patient and medication features are implemented.

A key design rule is:

```text
Hospital
   ├── Branch
   │    ├── Department
   │    └── Staff
   └── Other Branches
```

Another hospital has its own separate structure and data.

## Security

DrugReminder handles healthcare-related organizational information, so security must be considered throughout development.

Current security principles include:

- do not commit `.env` files or secrets;
- authenticate users before protected pages are accessed;
- use hospital membership and roles for authorization;
- use Supabase/PostgreSQL Row Level Security to help isolate hospital data;
- use database constraints to protect data integrity;
- preserve audit/history information instead of silently overwriting important healthcare events.

The application is still under development and should not yet be treated as a production-certified clinical system.

## Development Workflow

The agreed development workflow is:

```text
Build
  ↓
Test locally
  ↓
Verify database/Supabase behavior
  ↓
Commit/push the completed change to GitHub
  ↓
Continue to the next feature
```

Before pulling GitHub changes onto a computer that may contain manual edits, check:

```bash
git status
```

This helps prevent accidental loss of uncommitted local work.

To view the current branch:

```bash
git branch --show-current
```

To download remote changes after local work is safe/committed:

```bash
git pull origin main
```

## Troubleshooting

### `python: command not found`

On systems where `python` is not configured as a command, use:

```bash
python3 app.py
```

### `ModuleNotFoundError`

Make sure the virtual environment is activated and install dependencies:

```bash
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Supabase environment error

If the application reports that `SUPABASE_URL` or `SUPABASE_KEY` must be set, check that `.env` exists in the project root and contains the required values.

Do not paste those secret values into public issues, commits or screenshots.

### Flask page does not reflect a recent change

Restart the Flask development server if necessary, then refresh the browser. For browser-cached frontend files/behavior, a hard refresh can also help.

### Git refuses to pull because local files changed

Do not force or delete the files immediately. Run:

```bash
git status
```

Review and protect the local changes before synchronizing with GitHub.

## Project Documentation

The README is the practical front page of the repository: it explains what the project is, its current capabilities, setup, requirements, structure and how to run it.

For the much deeper beginner-friendly explanation of how DrugReminder was designed and built, including challenges, questions, decisions, lessons and detailed file explanations, read:

```text
docs/DRUGREMINDER_PROJECT_LEARNING_GUIDE.md
```

That learning guide is intentionally separate from the README and will grow throughout development.

---

## Current Status

**DrugReminder is under active development and is not yet production-ready.**

The goal is to build and verify the system feature by feature, while keeping both the source code and documentation understandable and up to date.
