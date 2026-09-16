# DrugReminder — Product Requirements Document (PRD)

**Version:** 1.0  
**Status:** Active Development  
**Backend:** Flask  
**Database:** PostgreSQL via Supabase  
**Repository:** `ejembiedwin36-oss/DrugReminder`  

## 1. Product Goal

DrugReminder is a hospital healthcare management platform designed to help hospitals manage patients, staff, medication schedules, reminders, medication administration, notifications, departments, branches, and hospital operations.

The central goal is to help ensure that the right patient receives the right medication at the right time through the right caregiver, with a reliable record of what happened.

## 2. Core Architecture

```text
User
  ↓
hospital_users
  ↓
Hospital
  ↓
Branch
  ↓
Department
  ↓
Staff / Patients / Medication
```

Each hospital's data must remain isolated from other hospitals.

## 3. Main Users

- Hospital Administrator
- Doctor
- Nurse
- Pharmacist
- Other Hospital Staff
- Patient

## 4. Hospital Requirements

A hospital supports:

- Hospital name
- Private or government type
- Phone
- Email
- Address
- Owner/manager
- Information
- Multiple branches

A hospital may have one headquarters and multiple branches. Each branch has its own address and operational information.

## 5. Departments

Current department types:

- Ward
- Pharmacy
- Emergency
- Other

A Ward is for admitted patients, Pharmacy handles medication-related activities, and Emergency handles serious/urgent cases.

## 6. Authentication and Ownership

Users create accounts through Supabase Auth and log in before using protected hospital features.

The intended flow is:

```text
Create Account
      ↓
Confirm Email if Required
      ↓
Login
      ↓
Dashboard
      ↓
Register Hospital
      ↓
Automatically become hospital_admin
      ↓
Register Branch
      ↓
Register Department
```

Hospital registration is performed through an authenticated Supabase function. Users must not be able to assign themselves to arbitrary hospitals.

## 7. Staff Management

Staff will include:

- Doctor
- Nurse
- Pharmacist
- Other staff

Staff records will include profile information, role, hospital, branch, department, and status.

Department transfers must preserve historical assignments. A transfer changes the current assignment without deleting the previous assignment.

## 8. Patient Management

Patient records will include relevant identity, location, date of birth, hospital, branch, and current care location information.

Patient data must obey hospital and branch isolation rules.

## 9. Medication Management

Medication schedules will connect:

```text
Patient
  ↓
Medication
  ↓
Method
  ↓
Scheduled Time
  ↓
Responsible Caregiver
  ↓
Reminder
  ↓
Administration
  ↓
Confirmation
```

The system should notify the responsible nurse approximately five minutes before the scheduled time.

## 10. Medication Monitoring

The system must support statuses such as:

- Scheduled
- Administered
- Confirmed
- Missed
- Not Confirmed

The system should distinguish medication administration from confirmation so that an administered medication that was not digitally confirmed is not automatically treated as medication that was never administered.

Missed or unconfirmed medication should notify appropriate responsible personnel, such as a doctor or Head Nurse. A reason may be recorded.

## 11. Automatic Nurse Assignment

Future automatic assignment should consider:

1. Workload
2. Location
3. Availability

If no suitable nurse is available, the system should notify the Head Nurse.

The system records events and alerts; management handles staff consequences.

## 12. Home Delivery

Patients will eventually be able to submit medication/home-delivery requests when they cannot attend the hospital.

The workflow will distinguish emergency and normal requests and require hospital review before delivery.

## 13. Security Requirements

Security is a core requirement.

- Supabase Authentication protects user accounts.
- Row Level Security protects hospital data.
- Hospital membership controls access to hospital resources.
- Roles control permissions.
- Anonymous users must not be able to create hospital ownership records.

## 14. Current Database Foundation

Implemented tables:

```text
hospitals
hospital_branches
departments
hospital_users
```

Implemented security foundation includes RLS, hospital membership, hospital-scoped branch/department access, and authenticated hospital registration.

## 15. Current Flask Foundation

Implemented routes include:

```text
/
/about
/signup
/login
/logout
/dashboard
/register-hospital
/register-branch/<hospital_id>
/register-department/<branch_id>
```

## 16. Current Development Status

### Completed

- Flask project foundation
- Supabase/PostgreSQL connection
- Environment-variable structure
- Hospitals table
- Hospital branches table
- Departments table
- Hospital users table
- Row Level Security foundation
- Hospital membership access rules
- Secure hospital registration function
- Signup page
- Login page
- Logout
- Dashboard
- Hospital registration flow
- Branch registration flow
- Department registration flow

### Current Phase

**Phase 1.8 — Authentication & Workflow Testing**

The next task is to verify the complete real-user workflow rather than assuming it works.

### Immediate Test

```text
Create Account
      ↓
Confirm Email if Required
      ↓
Login
      ↓
Dashboard
      ↓
Register Hospital
      ↓
Verify hospital_admin membership
      ↓
Register Branch
      ↓
Register Department
```

## 17. Next Major Phase

After Phase 1.8 passes testing:

**Phase 2 — Staff Management & Hospital Personnel**

Planned work:

- Staff table/design
- Staff profiles
- Staff roles
- Branch assignment
- Department assignment
- Current department
- Assignment history
- Staff transfers
- Hospital/branch isolation
- Foundation for workload, location, and availability

## 18. Overall Roadmap

```text
Phase 1  Foundation & Authentication
Phase 2  Staff Management
Phase 3  Patient Management
Phase 4  Medication Management
Phase 5  Medication Scheduling
Phase 6  Medication Reminders
Phase 7  Medication Confirmation & Monitoring
Phase 8  Automatic Nurse Assignment
Phase 9  Notifications & Alerts
Phase 10 Doctor & Clinical Management
Phase 11 Pharmacy Management
Phase 12 Home Delivery
Phase 13 Hospital Administration & Reports
Phase 14 Security Hardening & Testing
Phase 15 Production Preparation
```

## 19. Development Rule

Do not jump randomly between features. Each phase should follow:

```text
Plan
 ↓
Design
 ↓
Database
 ↓
Backend
 ↓
Frontend
 ↓
Security
 ↓
Testing
 ↓
Documentation
 ↓
Complete
```

Before moving to the next major phase, verify the current phase, fix discovered problems, and then continue.

## 20. Definition of Long-Term Success

A hospital should eventually be able to register, create branches and departments, manage staff and patients, create medication plans, assign caregivers, send reminders, record administration and confirmation, monitor missed activities, and manage home-delivery requests while maintaining strong hospital data isolation and reliable audit records.
