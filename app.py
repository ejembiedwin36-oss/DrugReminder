import os

from flask import Flask, render_template, request, redirect, url_for, session

from database import get_user_memberships
from database import register_branch as save_branch
from database import register_department as save_department
from database import register_hospital as save_hospital
from database import sign_in, sign_up


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY must be set")


def current_session():
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    if not access_token or not refresh_token:
        return None

    return access_token, refresh_token


def require_login():
    if not current_session():
        return redirect(url_for("login"))
    return None


@app.route("/")
def home():
    return "DrugReminder is running!"


@app.route("/about")
def about():
    return "Welcome to DrugReminder Healthcare Platform"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        try:
            response = sign_up(email, password)
        except Exception as error:
            return render_template("signup.html", error=str(error)), 400

        user = getattr(response, "user", None)
        auth_session = getattr(response, "session", None)

        if auth_session:
            session["access_token"] = auth_session.access_token
            session["refresh_token"] = auth_session.refresh_token
            return redirect(url_for("dashboard"))

        if user:
            return render_template(
                "login.html",
                error="Account created. Check your email to confirm it, then log in.",
            )

        return render_template("signup.html", error="Account creation failed."), 400

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        try:
            response = sign_in(email, password)
        except Exception as error:
            return render_template("login.html", error=str(error)), 401

        auth_session = getattr(response, "session", None)
        if not auth_session:
            return render_template(
                "login.html",
                error="Login did not create a session. Check your email confirmation and credentials.",
            ), 401

        session["access_token"] = auth_session.access_token
        session["refresh_token"] = auth_session.refresh_token
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    access_token, refresh_token = current_session()

    try:
        memberships = get_user_memberships(access_token, refresh_token)
    except Exception as error:
        return f"Could not load your hospital memberships: {error}", 500

    return render_template("dashboard.html", memberships=memberships)


@app.route("/register-hospital", methods=["GET", "POST"])
def register_hospital():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        hospital_name = request.form["hospital_name"].strip()
        hospital_type = request.form["hospital_type"].strip().lower()
        phone = request.form.get("phone_number", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form["address"].strip()
        owner_manager_name = request.form.get("owner_manager_name", "").strip()
        information = request.form.get("information", "").strip()

        if not hospital_name or not address:
            return "Hospital name and address are required.", 400

        if hospital_type not in ("private", "government"):
            return "Invalid hospital type.", 400

        access_token, refresh_token = current_session()

        try:
            result = save_hospital(
                access_token=access_token,
                refresh_token=refresh_token,
                hospital_name=hospital_name,
                hospital_type=hospital_type,
                phone=phone,
                email=email,
                address=address,
                owner_manager_name=owner_manager_name or None,
                information=information or None,
            )
        except Exception as error:
            return f"Hospital registration failed: {error}", 400

        hospital_id = result["hospital_id"]
        return redirect(url_for("register_branch", hospital_id=hospital_id))

    return render_template("register_hospital.html")


@app.route("/register-branch/<hospital_id>", methods=["GET", "POST"])
def register_branch(hospital_id):
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        branch_name = request.form["branch_name"].strip()
        address = request.form["address"].strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        location = request.form.get("location", "").strip()
        information = request.form.get("information", "").strip()
        is_headquarters = request.form.get("is_headquarters") == "true"

        if not branch_name or not address:
            return "Branch name and address are required.", 400

        access_token, refresh_token = current_session()

        try:
            save_branch(
                access_token=access_token,
                refresh_token=refresh_token,
                hospital_id=hospital_id,
                branch_name=branch_name,
                address=address,
                is_headquarters=is_headquarters,
                phone=phone or None,
                email=email or None,
                location=location or None,
                information=information or None,
            )
        except Exception as error:
            return f"Branch registration failed: {error}", 400

        return f"Branch '{branch_name}' registered successfully!"

    return render_template("register_branch.html", hospital_id=hospital_id)


@app.route("/register-department/<branch_id>", methods=["GET", "POST"])
def register_department(branch_id):
    redirect_response = require_login()
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        department_name = request.form["department_name"].strip()
        department_type = request.form["department_type"].strip().lower()
        description = request.form.get("description", "").strip()

        if not department_name:
            return "Department name is required.", 400

        if department_type not in ("ward", "pharmacy", "emergency", "other"):
            return "Invalid department type.", 400

        access_token, refresh_token = current_session()

        try:
            save_department(
                access_token=access_token,
                refresh_token=refresh_token,
                branch_id=branch_id,
                department_name=department_name,
                department_type=department_type,
                description=description or None,
            )
        except Exception as error:
            return f"Department registration failed: {error}", 400

        return f"Department '{department_name}' registered successfully!"

    return render_template("register_department.html", branch_id=branch_id)


if __name__ == "__main__":
    app.run(debug=True)
