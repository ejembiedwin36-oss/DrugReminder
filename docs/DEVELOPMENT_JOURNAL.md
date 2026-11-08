# DrugReminder — Development Journal and Lessons Learned

This is the chronological working log. Keep the existing [Project Learning Guide](DRUGREMINDER_PROJECT_LEARNING_GUIDE.md) as the fuller teaching reference. Update this journal with each meaningful development session, including what was attempted, actual results, errors, decisions, tests, commit IDs, and next actions. Never record passwords, API keys, refresh tokens, patient-identifying data, or private medical records.

## Historical recap (reported in prior sessions; not independently re-tested here)
- Hospital, branch, department and staff registration workflows were built with live form validation.
- Staff transfer was tested with fictional/test assignment data: switching branch changed the available department options, and the previous assignment remained in history.
- Patient Management Phase 1: patient and patient_branch_history tables, branch-scoped privacy rules, and patient registration code were reported implemented.
- Reported patient-registration commits: `8d4e4ec`, `afa59c4`, `4086c73`, `54582f7`. Verify their content against Git history before relying on them.
- A known issue remained: `Dashboard error: Invalid Refresh Token: Already Used`. A logout/login workaround was proposed, but a permanent session-handling fix and regression tests were not confirmed.

## 2026-11-08 — Reconnected project review
**Goal:** Resume DrugReminder directly through connected GitHub and Supabase, and maintain a comprehensive learning/error journal.

**Verified:**
- Connected GitHub account: `ejembiedwin36-oss`; repository `ejembiedwin36-oss/DrugReminder`, default branch `main`, write access available.
- Repository contains `app.py`, `database.py`, `templates/`, `README.md`, and existing `docs/DRUGREMINDER_PROJECT_LEARNING_GUIDE.md`.
- Supabase lists project `DrugReminder` (project ID `frkvuiqubaqvisiraxvp`) as `ACTIVE_HEALTHY`.

**Error / limitation:** Supabase table inspection failed with `Connection terminated due to connection timeout`. Project health alone does not prove database queries work. Do not infer data loss or successful table verification.

**Design decisions:** Patient details must be scoped to authorized care context; another branch must not automatically see them. Branch transfers require authorization and preserved audit history. Inter-hospital referrals need a separate controlled sharing workflow.

**Next steps:** Inspect Flask authentication and Supabase refresh-token handling; make the smallest safe fix; test login, expired/used-token behavior and dashboard access; verify patient registration and branch isolation; document tests and outcomes; push verified code changes.

## Journal entry template
### YYYY-MM-DD — Topic
- **Objective:**
- **Files/code changed and why:**
- **Commands or database migrations run:**
- **What succeeded (evidence):**
- **Mistakes/errors and exact sanitized messages:**
- **Root cause (confirmed vs suspected):**
- **Fix and why it works:**
- **Tests run and results:**
- **Insights / concepts learned:**
- **Git commit / PR:**
- **Remaining risks and next step:**
