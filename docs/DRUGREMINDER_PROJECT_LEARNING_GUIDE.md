# DrugReminder — Complete Project Learning Guide

> **Living document:** This file is updated as the project grows. Its purpose is to make the whole DrugReminder project understandable to a beginner, including what we built, why we built it, decisions we made, questions asked during planning, problems encountered, fixes, lessons learned, and how every important file works.

## 1. What is DrugReminder?

DrugReminder is a hospital medication-management and care-coordination web application. It is being designed so that different hospitals can adopt the system while keeping their information separate and secure.

A hospital can have several branches. Each branch can have departments. Staff and patients belong to the correct hospital/branch, and medication tasks can later be assigned to the appropriate healthcare workers.

The most important goal is not simply to display reminders. DrugReminder is intended to help hospitals know what medication was scheduled, who was responsible for administering it, whether it was administered and confirmed, what happened when a task was missed, and who needs to be notified.

## 2. The problem DrugReminder is solving

Hospital medication work involves people, time, responsibility and follow-up. A reminder alone is not enough. A hospital needs a reliable workflow around the reminder.

DrugReminder is therefore being designed around questions such as:

- Which patient needs medication?
- What medication, injection or drip should be given?
- At what time should it be given?
- Which nurse or caregiver is responsible?
- Was it actually confirmed as administered?
- What happens when it is not confirmed?
- Why was it missed?
- Who should be informed?
- Can another available nurse take over the task?
- Can the hospital later review what happened?

The system is intended to make this process more organized, visible and accountable.

## 3. Why the project can be helpful

DrugReminder can help a hospital organize hospitals, branches, departments, staff, patients and medication activities in one connected system. The planned reminder workflow includes a warning before medication time, an alert at the scheduled time, confirmation after administration, missed-task handling, escalation and an audit/history trail.

The project also preserves an important real-world distinction: one hospital organization may have many branches, but an entirely different hospital is a separate organization. Their information must not be mixed.

## 4. Important product decisions made during planning

### Hospital and branch separation

A major requirement was clarified using examples such as Faith Clinic Hospital and ABC Hospital. Faith Clinic may have branches in Kano, Lagos, Kogi and other places, but those branches still belong to Faith Clinic. ABC Hospital is a separate hospital. The application therefore needs both a hospital level and a branch level.

### Hospital data isolation

One hospital must not be able to see another hospital's private data. This requirement influenced the database design and the use of PostgreSQL Row Level Security (RLS) in Supabase.

### PostgreSQL/Supabase instead of SQLite

The project originally began as a simple Flask learning project, where SQLite was considered. The design later moved to PostgreSQL through Supabase because the application is intended to grow into a multi-hospital system with authentication, relationships and stronger access control.

### Staff history must not disappear after transfers

If a staff member moves from one department or branch to another, the old assignment should remain in history. The current assignment changes, but the historical record should remain available. This led to the `staff_assignments` concept.

### Medication confirmation matters

A nurse should not simply receive an alarm. After administering medication, the nurse should confirm the task. If the medicine was administered but the confirmation button was not clicked, the system needs an audit/correction path rather than silently treating the data as unquestionably correct.

### Missed medication should be recorded, not overwritten

If a 2:00 PM medication is missed and an authorized person reschedules it for 2:30 PM, the original 2:00 PM task should remain recorded as missed. The 2:30 PM task becomes a new scheduled task. This preserves accountability and history.

### Reassignment and escalation

The planned workflow first tries to reassign a missed/unavailable nursing task using factors such as availability, workload and location. If no suitable nurse is available, the issue should escalate to the Head Nurse/management.

## 5. Planned user roles

### Hospital Administrator
Manages hospital-level setup and administrative functions, including staff and organizational structure.

### Doctor
Planned responsibilities include viewing assigned patients, reviewing medication status, checking relevant hospital activity, assigning a nurse where authorized, and ensuring patient care is followed up.

### Nurse
Planned responsibilities include logging in, viewing duties for the day, receiving medication alerts, administering drugs/injections/drips according to instructions, and confirming completed tasks.

### Head Nurse / Management
Receives escalations for missed tasks and can participate in reassignment/approval workflows.

### Patient
The planned patient profile includes information such as name, address, email, personal ID and phone. Patient-facing request features are also planned.

## 6. Medication workflow vision

The intended end-to-end workflow is:

1. A medication task is scheduled for a patient.
2. A responsible caregiver is assigned.
3. The nurse receives a pre-notification about five minutes before the scheduled time.
4. An alarm/notification occurs at the scheduled time.
5. The nurse administers the medication according to the instruction.
6. The nurse confirms the task.
7. The system records the confirmation and keeps an audit/history record.
8. If confirmation does not happen, the task can become missed/not confirmed.
9. A reason is captured where appropriate.
10. The doctor and/or Head Nurse can be notified.
11. Reassignment or authorized rescheduling can happen without deleting the original history.

This is the heart of DrugReminder and is still under development.

## 7. Patient requests and future care workflow

The product requirements include an emergency portal/request path and a normal home-delivery request path. A structured request and messaging workflow is planned, with a doctor or other authorized hospital staff making the appropriate decision.

## 8. Technology used

### Python
Python is the main backend programming language.

### Flask
Flask is the web framework currently used to create routes, receive form data, manage sessions and render HTML templates.

### Supabase / PostgreSQL
Supabase provides the PostgreSQL database and authentication-related services. PostgreSQL stores structured application data and relationships.

### Row Level Security (RLS)
RLS is used to help enforce the rule that authenticated users should only access data belonging to hospitals they are authorized to access.

### HTML, CSS and JavaScript
HTML creates the form/page structure. CSS controls presentation. JavaScript is being used for live form validation so users can receive feedback while typing instead of discovering every format problem only after submitting a form.

### Git and GitHub
Git tracks changes to the source code. GitHub stores the project repository and its history. The agreed workflow is to build, test, verify Supabase behavior, and keep completed changes synchronized to GitHub.

## 9. Current database concepts

### `hospitals`
Represents a hospital organization. This is the top organizational level.

### `hospital_branches`
Represents individual branches belonging to a hospital.

### `departments`
Represents departments such as Ward, Pharmacy, Emergency or other units within a branch.

### `hospital_users`
Connects authenticated users to hospitals and records their role in that hospital.

### `staff`
Stores a staff member's current hospital, branch, department, role and profile information.

### `staff_assignments`
Preserves staff assignment/history information. This becomes important when staff transfer between departments or branches.

Additional patient, medication, schedule, confirmation, missed-task, reschedule, request and audit structures are part of the wider design and will be documented as they are implemented.

## 10. Current source files and what they do

This section must be updated whenever important files are added, renamed or significantly changed.

### `app.py`
This is currently the main Flask application file. It defines web routes and connects browser actions to database helper functions.

Examples of responsibilities currently handled here include signup/login, dashboard loading, hospital registration, branch registration, department registration, staff registration and the hospital staff list.

A Flask route can be understood as a doorway into the application. For example, when the browser requests a particular URL, Flask finds the matching route function and runs it.

### `database.py`
This file contains the Python functions that communicate with Supabase. Keeping database operations here prevents every Flask route from having to contain raw database-access logic.

Examples include authentication helpers, registering hospitals/branches/departments/staff, retrieving branches and departments, creating staff assignments and retrieving a hospital's staff.

A simple beginner mental model is:

`Browser -> Flask route in app.py -> database function in database.py -> Supabase/PostgreSQL -> result returns to Flask -> HTML page`

### `templates/`
Flask looks in this folder for HTML templates rendered by `render_template()`.

### `templates/register_hospital.html`
Contains the hospital registration user interface.

### `templates/register_branch.html`
Contains the branch registration user interface.

### `templates/register_department.html`
Contains the department registration user interface.

### `templates/register_staff.html`
Contains the staff registration form. Live validation has been added so common input problems can be reported while the user types. Validation can detect things such as required fields and invalid email/phone formats, but it cannot reliably know that every real person's name is spelled correctly.

### `templates/staff_list.html`
Displays staff belonging to a hospital, including useful current assignment information such as branch and department.

### `.env`
Used locally for environment variables such as configuration values and secrets. Secret values must not be committed to GitHub.

### `.gitignore`
Tells Git which local/generated/sensitive files should not be tracked, such as `.env`, Python cache files and the virtual environment.

### `venv/`
The Python virtual environment used on the development computer. It contains installed packages for the project. It is not application source code and should not be stored in GitHub.

## 11. Important questions asked during requirements discovery

This project has been shaped by questions rather than blindly writing code. Important discussions included:

### Are different hospitals separate, or are they branches of one hospital?
The answer established that hospitals such as Faith Clinic Hospital and ABC Hospital are separate organizations, while Faith Clinic itself can have many branches. This decision created the hospital/branch hierarchy.

### Should patients be separate from hospitals?
The requirement was clarified toward a separate patient concept/table connected to the appropriate hospital, rather than mixing patient records into hospital records.

### Should SQLite remain the database?
The decision was to use PostgreSQL through Supabase instead, because the project is intended to support a more serious multi-hospital architecture.

### What happens when a nurse misses a medication task?
The requirement developed into missed/not-confirmed tracking, reason capture, notification/escalation, possible reassignment and preservation of the original history.

### What happens if medication was administered but the nurse forgot to confirm it?
This exposed the need for discrepancy handling and an audit/correction path instead of assuming that database status always perfectly represents real-world events.

### What happens when staff transfer departments?
The answer established that old assignment history must remain while the current department changes. This influenced the `staff_assignments` table.

These requirement questions are important because they show that software design is not only coding. A developer must understand the real-world rules before choosing database tables and functions.

## 12. Challenges encountered so far and what they taught us

### Learning environment setup
An early challenge involved accidentally creating/mistyping an item called `vene` instead of correctly setting up `venv`. The incorrect item was removed, a Python virtual environment was created and activated, and Flask was installed. This taught an important beginner lesson: environment setup is part of software development, and small naming mistakes can affect commands and project structure.

### `render_template` error
During early Flask work, `render_template` was used before it was imported, causing a `NameError`. The fix was to import it from Flask. Lesson: Python must know where a function comes from before the program can use it.

### Moving from forms that only display to forms that save data
The first hospital registration work captured form information but did not yet have full persistence. The project gradually connected the form layer to Supabase. Lesson: an HTML form, a Flask route and a database are separate layers that must be connected deliberately.

### Multi-hospital isolation
A major design challenge was ensuring one hospital cannot access another hospital's information. The solution direction uses hospital IDs, membership records and Supabase/PostgreSQL RLS policies. Lesson: security and data ownership must be part of database design, not something added only at the end.

### Staff duplicate IDs
Registering an already-used staff ID triggered the PostgreSQL unique constraint `staff_hospital_id_staff_id_key`. Instead of exposing a technical database error to ordinary users, the application was changed to show a clearer message: the Staff ID is already registered and another ID should be used. Lesson: database constraints protect data, while application code should translate technical failures into understandable messages.

### Staff list did not initially show known records
Staff records existed in Supabase, but the GitHub version of `database.py` had not yet contained the new `get_hospital_staff()` work and local/GitHub versions were temporarily out of sync. This exposed an important development challenge: code can work or exist locally without being safely stored in the remote repository. The workflow was changed so completed work should be synchronized to GitHub.

### Live validation requirement
It became clear that users should not have to fill an entire form before discovering obvious format errors. Live JavaScript validation was added to staff registration. Lesson: backend validation protects the system, while immediate frontend feedback improves the user's experience. Both are useful and serve different purposes.

### Local code versus GitHub code
Some changes were made manually on the development laptop while other changes were pushed directly to GitHub. This creates a risk of competing versions. Lesson: source-control synchronization must be deliberate. Before pulling remote changes over local work, check Git status and protect uncommitted changes.

## 13. Security lessons already visible in the project

- Never commit `.env` secrets to GitHub.
- Authentication is not the same as authorization. Logging in proves who a user is; authorization determines what that user may access or change.
- Hospital isolation must be enforced at the database/security layer as well as in the user interface.
- Unique constraints are useful for protecting data integrity.
- Role permissions should be designed explicitly.
- Audit history is especially important when software represents healthcare actions.

## 14. How to understand DrugReminder as a beginner

Do not try to understand the entire application at once. Follow one request through the system.

Example: registering a staff member.

1. The user opens the staff registration page.
2. Flask runs the route in `app.py`.
3. Flask renders `register_staff.html`.
4. The user enters information.
5. JavaScript gives immediate feedback for common input errors.
6. The user submits the form.
7. Flask reads the submitted values.
8. `app.py` calls a function from `database.py`.
9. `database.py` sends the operation to Supabase.
10. PostgreSQL checks constraints and RLS rules.
11. The result returns to Python.
12. Flask redirects or renders the next page.
13. The staff list can read the stored data back and display it.

Once this flow makes sense, many other web application features become easier to understand because they follow the same broad pattern.

## 15. Current development status

The foundation is under active development. Authentication, hospital structure, branches, departments, staff registration, staff assignment foundations, security policies and staff listing work have been started/implemented to varying degrees.

The core medication-reminder engine is still ahead. Major remaining areas include complete staff management/transfers, patient management, medication definitions and schedules, notifications, confirmations, missed-task handling, reassignment/escalation, role-specific dashboards, patient requests, stronger audit/security work, testing, production UI and deployment.

A meaningful MVP milestone will be reached when the system can demonstrate a complete real-world path such as:

`Hospital -> Branch -> Department -> Doctor/Nurse -> Patient -> Medication Schedule -> 5-minute Alert -> Administration -> Confirmation -> Audit Record`

and also demonstrate what happens when that medication is missed or not confirmed.

## 16. Documentation rule for the rest of the project

As development continues, this guide should record:

- every important new feature;
- every important file and its responsibility;
- database tables and relationships;
- routes and how requests move through them;
- important functions and why they exist;
- requirements questions and the decisions produced by the answers;
- implementation problems, errors and their causes;
- how each problem was fixed;
- security decisions;
- testing lessons;
- Git/GitHub lessons;
- Supabase/database lessons;
- changes in architecture and why they were made;
- unfinished limitations and future improvements;
- a final beginner-friendly walkthrough of the completed system.

The final version should be detailed enough that a beginner can read it from the beginning and understand not only **what DrugReminder does**, but also **how and why it was built the way it was**.

---

**Status:** Living documentation — update throughout development.
