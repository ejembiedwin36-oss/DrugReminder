# DrugReminder — Complete Project Learning Guide

> **Living document:** This guide records not only what DrugReminder does, but how and why it is being built, the questions that shaped it, problems encountered, fixes, testing results and lessons for a beginner developer.

## 1. What is DrugReminder?

DrugReminder is a hospital medication-management and care-coordination web application. Different hospitals can adopt the system while keeping their information separate. A hospital can have multiple branches; branches can contain departments; staff can be assigned to the correct branch and department; and future medication tasks will connect patients, healthcare workers, schedules, reminders, confirmations and escalation.

The goal is bigger than an alarm. DrugReminder is intended to help answer: what was scheduled, for whom, when, who was responsible, whether it was administered/confirmed, what happened if it was missed, and who needs to act next.

## 2. Core problem and product decisions

### Multi-hospital separation
Faith Clinic Hospital and ABC Hospital are separate organizations. Faith Clinic itself may have branches in different locations. This produced the hierarchy `Hospital -> Branch -> Department` and the requirement that one hospital must not access another hospital's private data.

### PostgreSQL/Supabase instead of SQLite
The project moved from a simple Flask learning setup toward PostgreSQL through Supabase because the intended product needs authentication, relationships, hospital isolation and stronger database security.

### Staff history must survive transfers
When a staff member moves, the application must not erase where the person previously worked. The `staff` record represents the current assignment while `staff_assignments` preserves assignment history.

### Human-authorized staff changes
A staff transfer is an administrative decision made by an authorized hospital administrator. DrugReminder records and executes that selected change; it does not independently decide that an employee should be transferred.

### Medication history must also be preserved
The same history principle applies to future medication workflows. For example, if a 2:00 PM task is missed and an authorized person reschedules it for 2:30 PM, the original 2:00 PM event should remain recorded as missed rather than being overwritten.

## 3. Roles and planned medication workflow

Current/planned roles include Hospital Administrator, Doctor, Nurse, Head Nurse/Management and Patient.

The intended medication flow is:

1. Schedule medication for a patient.
2. Assign the responsible caregiver.
3. Notify the nurse about five minutes before the scheduled time.
4. Alert at the scheduled time.
5. Nurse administers medication according to instruction.
6. Nurse confirms administration.
7. System preserves confirmation/audit information.
8. If confirmation does not happen, record missed/not-confirmed status.
9. Capture a reason where appropriate.
10. Notify/escalate to authorized clinical leadership.
11. Permit appropriate reassignment or authorized rescheduling without deleting history.

This medication engine is still future work.

## 4. Technology and beginner mental model

- **Python** — backend language.
- **Flask** — routes, forms, sessions and templates.
- **Supabase/PostgreSQL** — authentication, relational data and database security.
- **RLS** — helps enforce hospital data isolation.
- **HTML/CSS** — page structure/presentation.
- **JavaScript** — browser behavior and live validation.
- **Git/GitHub** — source history and remote repository.

A useful mental model is:

```text
Browser
  -> Flask route in app.py
  -> helper in database.py
  -> Supabase/PostgreSQL
  -> result back to Flask
  -> HTML response/redirect
```

## 5. Current database concepts

### `hospitals`
Top-level hospital organizations.

### `hospital_branches`
Branches belonging to hospitals.

### `departments`
Departments belonging to branches, such as Ward, Pharmacy and Emergency.

### `hospital_users`
Connects authenticated users to hospitals and roles.

### `staff`
Stores the staff member's current hospital, branch, department, role and profile data.

### `staff_assignments`
Stores current and previous staff assignments. A current assignment has no end time; a previous assignment has an `ended_at` value. Transfer reasons can be preserved for audit/history.

A unique-current-assignment rule prevents multiple simultaneous current assignment-history rows for one staff member.

## 6. Important source files

### `app.py`
Main Flask application. Current responsibilities include signup/login/logout, dashboard, hospital/branch/department registration, staff registration, staff listing, staff detail/history and staff transfer routes.

The transfer route reads the administrator's selected branch. When the branch changes, the route loads departments belonging to that branch. On submission it calls the database transfer helper and redirects back to staff details after success.

### `database.py`
Contains Supabase communication helpers. Important staff functions include:

- registering staff;
- creating the initial assignment;
- listing hospital staff;
- loading one staff member;
- loading assignment history;
- calling the secure `transfer_staff` PostgreSQL function.

Keeping this logic separate from Flask routes makes responsibilities easier to understand.

### `templates/dashboard.html`
Shows hospital membership information and administrative navigation such as View Staff, Register Staff and Register Branch.

### `templates/register_branch.html`
Branch registration form. Live validation was added for important fields. A checkbox indicates whether the branch is headquarters.

### `templates/register_department.html`
Department registration form. It was upgraded during testing with clearer layout and immediate validation of department name/type.

### `templates/register_staff.html`
Staff registration form with live validation for common input problems.

### `templates/staff_list.html`
Shows hospital staff, current branch/department and a link to each staff detail page.

### `templates/staff_detail.html`
Shows current staff information plus assignment history. History rows identify `Current` versus `Previous` assignments and display transfer reasons where available.

### `templates/transfer_staff.html`
Provides branch, department, role and transfer-reason fields. It validates the transfer reason while typing. Changing the branch reloads the page with departments for that branch, preventing the old branch's department list from remaining on screen.

### `.env` and `.gitignore`
`.env` contains local configuration/secrets and must not be committed. `.gitignore` keeps secrets, caches and the local virtual environment out of source control.

## 7. Staff transfer architecture — what actually happens

The staff transfer feature is an important example of connecting UI, Flask, Python and PostgreSQL.

```text
Hospital administrator opens Staff Details
                ↓
Clicks Transfer / Change Assignment
                ↓
Chooses destination branch
                ↓
Flask reloads departments for that branch
                ↓
Administrator chooses department + role
                ↓
Administrator enters transfer reason
                ↓
Flask calls database.py transfer_staff()
                ↓
Supabase calls PostgreSQL transfer_staff RPC
                ↓
Database verifies authorization and relationships
                ↓
Old current assignment receives ended_at + reason
                ↓
staff current branch/department/role is updated
                ↓
New current staff_assignments row is inserted
                ↓
Staff Details displays new current + old previous assignment
```

The database function performs the connected data changes atomically: either the operation succeeds together or an error prevents a partially completed transfer.

The function also checks that the authenticated user is a hospital administrator for the staff member's hospital, that the destination branch belongs to that hospital, that the selected department belongs to the destination branch, and that the role is permitted. It rejects an assignment that is exactly the same as the current one.

## 8. End-to-end transfer test completed on 16 October 2026

A real development test was performed using test organizational data.

The test created a second branch named `Faith Clinic Makurdi Test Branch` and a department named `General Ward Test`. Mary John (`FCN-001`) originally had the current assignment:

```text
edi-clinc -> Emergency -> Nurse
```

The administrator selected:

```text
Faith Clinic Makurdi Test Branch -> General Ward Test -> Nurse
```

with the test reason:

```text
Reassigned to the Makurdi test branch for staff transfer testing.
```

The application reported `Staff transfer completed successfully.` The Staff Details screen then showed Mary with the new branch and department. Assignment History showed the new Makurdi/General Ward assignment as `Current`, while `edi-clinc/Emergency/Nurse` had an ending timestamp, preserved transfer reason and `Previous` status.

This proved the full path from browser form through Flask/Supabase/PostgreSQL and back to the history screen.

## 9. Problems encountered during the transfer work

### Problem: same assignment rejected
The first attempted transfer used the same branch, department and role. PostgreSQL returned that the new assignment was the same as the current assignment.

**Lesson:** this was correct behavior, not a broken feature. A transfer must actually change assignment information.

### Problem: only one useful branch existed
To test a real branch transfer, a second branch was needed. A clearly marked test branch was created rather than pretending a transfer occurred.

**Lesson:** good testing requires data that can exercise the behavior being tested.

### Problem: branch form UI was basic
The branch registration page initially had a very plain layout. It was improved and live validation was tested. While typing the first character of a branch name, the form correctly warned that at least two characters were required, then became valid once enough text was entered.

**Lesson:** live validation is supposed to respond during typing; an early warning can disappear as soon as the value becomes valid.

### Problem: department form was still old/basic
After the test branch was created, the Register Department screen revealed that this form had not received the same validation/UI improvements. It was updated in GitHub, pulled locally and successfully used to create `General Ward Test`.

**Lesson:** end-to-end testing often reveals unfinished neighboring screens that isolated code review misses.

### Problem: changing branch left `Emergency` visible
This was the most important transfer UI bug. After selecting the new Makurdi branch, the department dropdown still showed `Emergency`, which belonged to the old `edi-clinc` branch.

**Cause:** departments were loaded when Flask rendered the page, but changing the HTML branch dropdown did not request a fresh department list.

**Fix:** the branch selector now updates the URL with the selected `branch_id`. Flask reads that branch, retrieves its departments and renders the transfer page again. After the fix, choosing `Faith Clinic Makurdi Test Branch` correctly displayed `General Ward Test`.

**Lesson:** relational rules must be reflected in the UI as well as the database. The database already protected the branch/department relationship, but the interface should guide the administrator toward valid choices before submission.

### Problem: `httpx.ReadTimeout`
A request timed out during testing.

**Lesson:** a network/client timeout is different from the database rejecting business logic. Developers should distinguish connectivity problems from validation/authorization problems.

### Problem: `Refresh Token: Already Used`
A stale/reused authentication session produced a refresh-token error.

**Lesson:** authentication state can expire or become invalid independently of the feature being tested. Returning to a fresh login/session is safer than misdiagnosing the staff feature.

### Problem: login appeared to erase credentials
Earlier, login failure looked like the form simply cleared. The login page was improved to show the actual authentication error while preserving the entered email.

**Lesson:** error messages are part of debugging and user experience. A failure should explain itself instead of appearing to do nothing.

## 10. Other important challenges and lessons

- `render_template` once caused a `NameError` because it was not imported. Python must know where a function comes from before use.
- Staff duplicate IDs are protected by a PostgreSQL unique constraint. Application code translates the technical error into a user-friendly message.
- Staff rows existed in Supabase while local/GitHub code temporarily differed. This reinforced the rule that completed changes must be pushed to GitHub.
- Live validation improves user experience, but backend/database validation remains necessary for security and integrity.
- Local changes and remote GitHub changes must be synchronized deliberately. Use `git status` before potentially conflicting pulls.

## 11. Requirements questions that shaped the design

Important questions included:

- Are different hospitals separate organizations or branches? Result: both hospital and branch levels are required.
- Should patients be a separate concept connected to hospitals? Result: yes, patient records should be modeled separately and related appropriately.
- Should the database remain SQLite? Result: PostgreSQL/Supabase was selected.
- What happens when medication is missed? Result: preserve missed history, capture reasons and support escalation/reassignment/rescheduling.
- What if medication was administered but confirmation was forgotten? Result: future discrepancy/audit correction path is required.
- What happens when staff move? Result: current assignment changes but historical assignments remain.
- Should the system decide employment transfers itself? Result: no; an authorized human administrator chooses the staff assignment change and DrugReminder securely records it.

## 12. Security lessons

- Authentication answers who the user is; authorization answers what that user may do.
- Never commit `.env` secrets.
- Hospital isolation belongs at the database/security layer, not only in hidden buttons/pages.
- Foreign-key relationships and constraints protect data integrity.
- RLS helps isolate hospital data.
- Sensitive multi-record operations should avoid partial updates; the staff transfer uses an atomic database function.
- Audit/history is important when software represents healthcare and administrative actions.

DrugReminder is still a development project and is not yet a production-certified clinical system.

## 13. How a beginner should study this project

Follow one workflow at a time. For staff transfer, ask these questions in order:

1. Which HTML page did the administrator use?
2. Which Flask route received the request?
3. What values did Flask read?
4. Which database helper did Flask call?
5. What did PostgreSQL verify/change?
6. Where did the browser redirect?
7. How did the history page prove the change worked?

This method is easier than trying to memorize the entire repository at once.

## 14. Current status after transfer testing

Working/tested foundation now includes authentication, hospital membership/dashboard, branches, departments, staff registration, staff listing, staff detail pages, assignment history and an end-to-end staff transfer workflow with branch-aware departments and preserved history.

Major work still ahead includes patient management, doctor/patient relationships, medication definitions and schedules, reminders, confirmation, missed/not-confirmed handling, clinical escalation, appropriate task reassignment, role-specific dashboards, patient requests, broader testing, production UI and deployment.

A future major milestone remains:

```text
Hospital -> Branch -> Department -> Doctor/Nurse -> Patient
-> Medication Schedule -> 5-minute Alert -> Administration
-> Confirmation -> Audit Record
```

plus the complete missed/not-confirmed path.

## 15. Documentation rule

Continue recording every important feature, file, database relationship, requirements decision, error, cause, fix, security decision and testing lesson. The final guide should allow a beginner to explain both **what DrugReminder does** and **why/how it was built this way**.

---

**Status:** Living documentation — staff transfer/history milestone tested successfully; continue updating throughout development.
