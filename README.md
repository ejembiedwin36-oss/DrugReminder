# DrugReminder

DrugReminder is a hospital medication-management and care-coordination web application built with Python, Flask, Supabase and PostgreSQL.

The project is designed for hospitals that need a structured way to manage branches, departments, staff, patients and medication activities while keeping each hospital's data separate and secure.

> **Project status:** Active development. The hospital and staff-management foundation is working, including a tested staff transfer/history workflow. Patient management and the complete medication reminder, confirmation, missed-task and escalation workflows are still under development.

## What DrugReminder Does

DrugReminder is intended to help hospitals organize medication-related responsibilities and follow-up. The finished workflow is intended to answer questions such as which patient needs medication, what should be administered, when it is due, who is responsible, whether it was confirmed, and what happens when a task is missed.

DrugReminder is a multi-hospital system. One hospital may have several branches, while a completely different hospital remains a separate organization and should not have access to another hospital's private information.

## Current Features

The project currently includes:

- Flask web application and Supabase authentication;
- hospital registration and hospital membership handling;
- hospital branch registration;
- department registration;
- staff registration and duplicate Staff ID protection;
- hospital staff listing and individual staff detail pages;
- current branch, department and role information;
- staff assignment history;
- hospital-admin initiated staff transfer/change of assignment;
- preservation of the previous assignment after a transfer;
- transfer reason/audit information;
- branch-aware department selection during transfers;
- live validation on important registration/transfer forms;
- PostgreSQL/Supabase data storage;
- Row Level Security and database authorization rules for hospital isolation.

### Staff transfer workflow — tested

The transfer workflow has been tested end to end. A hospital administrator can choose a new branch, choose a department belonging to that branch, keep or change the staff role, enter a transfer reason, and complete the reassignment.

The database preserves the previous assignment instead of deleting it. The old assignment receives an end time and becomes `Previous`; the new assignment becomes `Current`.

During testing, changing the branch initially left the old branch's department visible. This was fixed so changing the branch reloads the department list and only shows departments belonging to the selected branch.

## Planned Features

Major features still being developed include:

- patient registration and management;
- doctor-to-patient relationships;
- medication and dosage management;
- medication scheduling;
- five-minute pre-notifications;
- scheduled-time medication alerts;
- nurse administration confirmation;
- missed/not-confirmed medication tracking and reason capture;
- doctor/Head Nurse escalation;
- nurse task reassignment based on permitted operational factors such as availability, workload and location;
- authorized rescheduling while preserving the original missed record;
- patient emergency and normal/home-delivery requests;
- role-specific dashboards;
- broader audit trail and reporting;
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
| GitHub | Remote repository and collaboration |

## Project Structure

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
    ├── staff_list.html
    ├── staff_detail.html
    └── transfer_staff.html
```

### Important files

**`app.py`** — Main Flask application. It contains routes that receive browser requests, process forms, call database functions and render/redirect pages. It also contains the current staff-list, staff-detail and transfer routes.

**`database.py`** — Contains functions used by Flask to communicate with Supabase, including staff retrieval, assignment-history retrieval and the secure staff-transfer RPC call.

**`templates/transfer_staff.html`** — Staff transfer form. Changing the branch refreshes the page with departments belonging to that selected branch. It also validates the transfer reason while the administrator types.

**`templates/staff_detail.html`** — Displays the staff member's current information and assignment history, including Current/Previous status.

**`docs/DRUGREMINDER_PROJECT_LEARNING_GUIDE.md`** — Detailed beginner-friendly project explanation, decisions, problems, fixes, testing and lessons.

## Requirements and Installation

Before running locally, install Python 3 and Git.

```bash
git clone https://github.com/ejembiedwin36-oss/DrugReminder.git
cd DrugReminder
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

If the repository is already cloned, do not clone it again. Enter the existing folder, activate its environment and pull safe remote changes when appropriate.

## Environment Variables

Create `.env` in the project root. Never commit it or share its secret values publicly.

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_or_anon_key
FLASK_SECRET_KEY=your_private_random_flask_secret
```

## Running the Application

```bash
source venv/bin/activate
python3 app.py
```

The Flask development server normally runs at `http://127.0.0.1:5000` in the current setup. Stop it with `Ctrl + C`.

## Basic Application Flow

```text
Browser
   ↓
HTML template / form
   ↓
Flask route (app.py)
   ↓
Database helper (database.py)
   ↓
Supabase / PostgreSQL
   ↓
Database constraints, RLS and secure functions
   ↓
Result returns to Flask
   ↓
Flask renders or redirects
```

### Current staff transfer flow

```text
Dashboard
   ↓
View Staff
   ↓
Staff Details
   ↓
Transfer / Change Assignment
   ↓
Choose new branch
   ↓
Load departments belonging to that branch
   ↓
Choose department and role
   ↓
Enter transfer reason
   ↓
Secure database transfer function
   ↓
Close previous assignment
   ↓
Update current staff assignment
   ↓
Create new assignment-history record
   ↓
Return to Staff Details
```

Staff transfers are authorized human administrative actions. DrugReminder records and executes the administrator's selected reassignment; it does not independently decide that an employee should be transferred.

## Database and Security

Current core concepts include:

- `hospitals`
- `hospital_branches`
- `departments`
- `hospital_users`
- `staff`
- `staff_assignments`

Important security principles include authentication, hospital membership, role-based authorization, PostgreSQL constraints, Row Level Security, secure server/database operations, and preservation of important history rather than silently overwriting it.

The staff transfer operation uses a database function so the related history/current-assignment changes are handled together. It verifies the staff member, hospital administrator authorization, target branch/hospital relationship, target department/branch relationship and permitted staff role.

DrugReminder is still under development and should not yet be treated as a production-certified clinical system.

## Development Workflow

The agreed workflow is:

```text
Build
  ↓
Test locally
  ↓
Verify Supabase/database behavior
  ↓
Push completed changes to GitHub
  ↓
Update documentation
  ↓
Continue
```

Before pulling when local edits may exist, use `git status`. To download completed remote changes after local work is safe, use `git pull origin main`.

## Troubleshooting Lessons

### Login fields appeared to disappear
The login page originally did not make authentication failures clear. Error display was improved, which exposed invalid credentials instead of silently appearing to clear the form.

### `Refresh Token: Already Used`
A stale/reused authentication session can cause Supabase refresh-token errors. Returning to a fresh login/session resolves the authentication state rather than treating the error as a branch/staff problem.

### `httpx.ReadTimeout`
A network/database request can time out. This is different from a validation failure and should not be confused with the database rejecting a transfer.

### Transfer says the assignment is the same
The database intentionally rejects a transfer when branch, department and role are unchanged. A transfer must represent a real assignment change.

### Wrong departments after changing branch
The first transfer form kept the departments loaded for the old branch. The form was corrected so a branch change reloads departments for the newly selected branch only.

## Project Documentation

This README is the practical repository front page. For the detailed beginner-friendly history of the project—including requirements decisions, bugs, fixes, testing and explanations of important files—read `docs/DRUGREMINDER_PROJECT_LEARNING_GUIDE.md`.

---

**Current status:** Hospital/branch/department setup, staff registration/listing/details and the staff transfer/history workflow are functioning and have been tested. The next major development areas are patient management and the medication workflow.
