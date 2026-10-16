import os

from flask import Flask, render_template, request, redirect, url_for, session

from database import (
    sign_up, sign_in, register_hospital, register_branch, register_department,
    get_user_memberships, get_hospital_branches, get_branch_departments,
    register_staff, create_staff_assignment, get_hospital_staff,
    get_staff_member, get_staff_assignment_history, transfer_staff,
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-secret-key")


def login_tokens():
    return session.get("access_token"), session.get("refresh_token")


@app.route("/")
def home():
    return "DrugReminder is running!"


@app.route("/about")
def about():
    return "Welcome to DrugReminder Healthcare Platform"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = None
    if request.method == "POST":
        try:
            sign_up(request.form.get("email"), request.form.get("password"))
            message = "Account created. You can now log in."
        except Exception as error:
            message = str(error)
    return render_template("signup.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        try:
            response = sign_in(request.form.get("email"), request.form.get("password"))
            if response.session:
                session["access_token"] = response.session.access_token
                session["refresh_token"] = response.session.refresh_token
                return redirect(url_for("dashboard"))
            message = "Login failed."
        except Exception as error:
            message = str(error)
    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    try:
        memberships = get_user_memberships(access_token, refresh_token)
        return render_template("dashboard.html", memberships=memberships)
    except Exception as error:
        app.logger.exception("Dashboard failed to load")
        return f"Dashboard error: {error}", 500


@app.route("/register-hospital", methods=["GET", "POST"])
def register_hospital_route():
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    message = None
    if request.method == "POST":
        try:
            result = register_hospital(
                access_token, refresh_token, request.form.get("hospital_name"),
                request.form.get("hospital_type"), request.form.get("phone_number"),
                request.form.get("email"), request.form.get("address"),
                request.form.get("owner_manager_name"), request.form.get("information"),
            )
            return redirect(url_for("register_branch_route", hospital_id=result["hospital_id"]))
        except Exception as error:
            message = str(error)
    return render_template("register_hospital.html", message=message)


@app.route("/register-branch/<hospital_id>", methods=["GET", "POST"])
def register_branch_route(hospital_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    message = None
    if request.method == "POST":
        try:
            branches = register_branch(
                access_token, refresh_token, hospital_id, request.form.get("branch_name"),
                request.form.get("address"), request.form.get("is_headquarters") == "on",
                request.form.get("phone"), request.form.get("email"),
                request.form.get("location"), request.form.get("information"),
            )
            if branches:
                return redirect(url_for("register_department_route", branch_id=branches[0]["id"]))
            message = "Branch could not be created."
        except Exception as error:
            message = str(error)
    return render_template("register_branch.html", hospital_id=hospital_id, message=message)


@app.route("/register-department/<branch_id>", methods=["GET", "POST"])
def register_department_route(branch_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    message = None
    if request.method == "POST":
        try:
            register_department(
                access_token, refresh_token, branch_id, request.form.get("department_name"),
                request.form.get("department_type"), request.form.get("description"),
            )
            message = "Department registered successfully."
        except Exception as error:
            message = str(error)
    return render_template("register_department.html", branch_id=branch_id, message=message)


@app.route("/register-staff/<hospital_id>", methods=["GET", "POST"])
def register_staff_route(hospital_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    message = None
    try:
        branches = get_hospital_branches(access_token, refresh_token, hospital_id)
    except Exception as error:
        return render_template("register_staff.html", hospital_id=hospital_id, branches=[], departments=[], message=str(error))

    selected_branch_id = request.form.get("branch_id") or (branches[0]["id"] if branches else None)
    departments = []
    if selected_branch_id:
        try:
            departments = get_branch_departments(access_token, refresh_token, selected_branch_id)
        except Exception as error:
            message = str(error)

    if request.method == "POST":
        department_id = request.form.get("department_id") or None
        try:
            created_staff = register_staff(
                access_token, refresh_token, hospital_id, selected_branch_id, department_id,
                request.form.get("full_name"), request.form.get("staff_id"), request.form.get("role"),
                request.form.get("phone"), request.form.get("email"), request.form.get("address"),
            )
            if created_staff:
                create_staff_assignment(
                    access_token, refresh_token, created_staff[0]["id"], hospital_id,
                    selected_branch_id, department_id, request.form.get("role"),
                )
                return redirect(url_for("staff_list", hospital_id=hospital_id, registered="1"))
            message = "Staff member could not be registered."
        except Exception as error:
            error_text = str(error)
            message = "This Staff ID is already registered. Please use a different Staff ID." if "duplicate" in error_text.lower() else error_text

    return render_template(
        "register_staff.html", hospital_id=hospital_id, branches=branches,
        departments=departments, selected_branch_id=selected_branch_id, message=message,
    )


@app.route("/staff/<hospital_id>")
def staff_list(hospital_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    message = "Staff member registered successfully." if request.args.get("registered") == "1" else None
    try:
        staff_members = get_hospital_staff(access_token, refresh_token, hospital_id)
    except Exception as error:
        staff_members = []
        message = f"Could not load staff: {error}"
    return render_template("staff_list.html", hospital_id=hospital_id, staff_members=staff_members, message=message)


@app.route("/staff/<hospital_id>/<staff_record_id>")
def staff_detail(hospital_id, staff_record_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    try:
        staff_member = get_staff_member(access_token, refresh_token, hospital_id, staff_record_id)
        if not staff_member:
            return "Staff member not found or you do not have access.", 404
        history = get_staff_assignment_history(access_token, refresh_token, hospital_id, staff_record_id)
        message = "Staff transfer completed successfully." if request.args.get("transferred") == "1" else None
        return render_template("staff_detail.html", hospital_id=hospital_id, staff=staff_member, assignment_history=history, message=message)
    except Exception as error:
        return render_template("staff_detail.html", hospital_id=hospital_id, staff=None, assignment_history=[], message=f"Could not load staff details: {error}")


@app.route("/staff/<hospital_id>/<staff_record_id>/transfer", methods=["GET", "POST"])
def transfer_staff_route(hospital_id, staff_record_id):
    access_token, refresh_token = login_tokens()
    if not access_token or not refresh_token:
        return redirect(url_for("login"))
    try:
        staff_member = get_staff_member(access_token, refresh_token, hospital_id, staff_record_id)
        if not staff_member:
            return "Staff member not found or you do not have access.", 404
        branches = get_hospital_branches(access_token, refresh_token, hospital_id)
    except Exception as error:
        return str(error), 400

    selected_branch_id = (
        request.form.get("branch_id")
        or request.args.get("branch_id")
        or staff_member.get("branch_id")
    )

    try:
        departments = (
            get_branch_departments(access_token, refresh_token, selected_branch_id)
            if selected_branch_id else []
        )
    except Exception as error:
        departments = []
        message = f"Could not load departments: {error}"
    else:
        message = None

    if request.method == "POST":
        reason = (request.form.get("transfer_reason") or "").strip()
        if not reason:
            message = "Please enter a reason for the transfer."
        else:
            try:
                transfer_staff(
                    access_token, refresh_token, staff_record_id, selected_branch_id,
                    request.form.get("department_id") or None, request.form.get("role"), reason,
                )
                return redirect(url_for("staff_detail", hospital_id=hospital_id, staff_record_id=staff_record_id, transferred="1"))
            except Exception as error:
                message = str(error)

    return render_template(
        "transfer_staff.html", hospital_id=hospital_id, staff=staff_member,
        branches=branches, departments=departments,
        selected_branch_id=selected_branch_id, message=message,
    )


if __name__ == "__main__":
    app.run(debug=True)
