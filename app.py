import os

from flask import Flask, render_template, request, redirect, url_for, session

from database import (
    sign_up,
    sign_in,
    register_hospital,
    register_branch,
    register_department,
    get_user_memberships,
    get_hospital_branches,
    get_branch_departments,
    register_staff,
    create_staff_assignment,
)


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-secret-key")


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
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            sign_up(email, password)
            message = "Account created. You can now log in."

        except Exception as error:
            message = str(error)

    return render_template(
        "signup.html",
        message=message,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            response = sign_in(email, password)

            if response.session:
                session["access_token"] = response.session.access_token
                session["refresh_token"] = response.session.refresh_token

                return redirect(url_for("dashboard"))

            message = "Login failed."

        except Exception as error:
            message = str(error)

    return render_template(
        "login.html",
        message=message,
    )


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return redirect(url_for("login"))

    try:
        memberships = get_user_memberships(
            access_token,
            refresh_token,
        )

        return render_template(
            "dashboard.html",
            memberships=memberships,
        )

    except Exception:
        session.clear()

        return redirect(url_for("login"))


@app.route("/register-hospital", methods=["GET", "POST"])
def register_hospital_route():
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        hospital_name = request.form.get("hospital_name")
        hospital_type = request.form.get("hospital_type")
        phone = request.form.get("phone_number")
        email = request.form.get("email")
        address = request.form.get("address")
        owner_manager_name = request.form.get("owner_manager_name")
        information = request.form.get("information")

        try:
            result = register_hospital(
                access_token,
                refresh_token,
                hospital_name,
                hospital_type,
                phone,
                email,
                address,
                owner_manager_name,
                information,
            )

            hospital_id = result["hospital_id"]

            return redirect(
                url_for(
                    "register_branch_route",
                    hospital_id=hospital_id,
                )
            )

        except Exception as error:
            message = str(error)

    return render_template(
        "register_hospital.html",
        message=message,
    )


@app.route(
    "/register-branch/<hospital_id>",
    methods=["GET", "POST"],
)
def register_branch_route(hospital_id):
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        branch_name = request.form.get("branch_name")
        address = request.form.get("address")

        is_headquarters = (
            request.form.get("is_headquarters") == "on"
        )

        phone = request.form.get("phone")
        email = request.form.get("email")
        location = request.form.get("location")
        information = request.form.get("information")

        try:
            branches = register_branch(
                access_token,
                refresh_token,
                hospital_id,
                branch_name,
                address,
                is_headquarters,
                phone,
                email,
                location,
                information,
            )

            if branches:
                branch_id = branches[0]["id"]

                return redirect(
                    url_for(
                        "register_department_route",
                        branch_id=branch_id,
                    )
                )

            message = "Branch could not be created."

        except Exception as error:
            message = str(error)

    return render_template(
        "register_branch.html",
        hospital_id=hospital_id,
        message=message,
    )


@app.route(
    "/register-department/<branch_id>",
    methods=["GET", "POST"],
)
def register_department_route(branch_id):
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return redirect(url_for("login"))

    message = None

    if request.method == "POST":
        department_name = request.form.get("department_name")
        department_type = request.form.get("department_type")
        description = request.form.get("description")

        try:
            register_department(
                access_token,
                refresh_token,
                branch_id,
                department_name,
                department_type,
                description,
            )

            message = "Department registered successfully."

        except Exception as error:
            message = str(error)

    return render_template(
        "register_department.html",
        branch_id=branch_id,
        message=message,
    )


@app.route(
    "/register-staff/<hospital_id>",
    methods=["GET", "POST"],
)
def register_staff_route(hospital_id):
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return redirect(url_for("login"))

    message = None

    try:
        branches = get_hospital_branches(
            access_token,
            refresh_token,
            hospital_id,
        )

    except Exception as error:
        return render_template(
            "register_staff.html",
            hospital_id=hospital_id,
            branches=[],
            departments=[],
            message=str(error),
        )

    selected_branch_id = request.form.get("branch_id")

    if not selected_branch_id and branches:
        selected_branch_id = branches[0]["id"]

    departments = []

    if selected_branch_id:
        try:
            departments = get_branch_departments(
                access_token,
                refresh_token,
                selected_branch_id,
            )

        except Exception as error:
            message = str(error)

    if request.method == "POST":
        full_name = request.form.get("full_name")
        staff_number = request.form.get("staff_id")
        role = request.form.get("role")
        department_id = request.form.get("department_id")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")

        if department_id == "":
            department_id = None

        try:
            created_staff = register_staff(
                access_token,
                refresh_token,
                hospital_id,
                selected_branch_id,
                department_id,
                full_name,
                staff_number,
                role,
                phone,
                email,
                address,
            )

            if created_staff:
                new_staff_id = created_staff[0]["id"]

                create_staff_assignment(
                    access_token,
                    refresh_token,
                    new_staff_id,
                    hospital_id,
                    selected_branch_id,
                    department_id,
                    role,
                )

                message = "Staff member registered successfully."

            else:
                message = "Staff member could not be registered."

        except Exception as error:
            message = str(error)

    return render_template(
        "register_staff.html",
        hospital_id=hospital_id,
        branches=branches,
        departments=departments,
        selected_branch_id=selected_branch_id,
        message=message,
    )


if __name__ == "__main__":
    app.run(debug=True)