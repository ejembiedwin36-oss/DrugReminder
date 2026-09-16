from flask import Flask, render_template, request, redirect, url_for

from database import register_branch as save_branch
from database import register_hospital as save_hospital


app = Flask(__name__)


@app.route("/")
def home():
    return "DrugReminder is running!"


@app.route("/about")
def about():
    return "Welcome to DrugReminder Healthcare Platform"


@app.route("/register-hospital", methods=["GET", "POST"])
def register_hospital():
    if request.method == "POST":
        hospital_name = request.form["hospital_name"].strip()
        hospital_type = request.form["hospital_type"].strip().lower()
        phone = request.form.get("phone_number", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form["address"].strip()

        if not hospital_name or not address:
            return "Hospital name and address are required.", 400

        if hospital_type not in ("private", "government"):
            return "Invalid hospital type.", 400

        hospitals = save_hospital(
            hospital_name=hospital_name,
            hospital_type=hospital_type,
            phone=phone,
            email=email,
            address=address,
        )

        if not hospitals:
            return "Hospital registration failed.", 500

        hospital_id = hospitals[0]["id"]
        return redirect(url_for("register_branch", hospital_id=hospital_id))

    return render_template("register_hospital.html")


@app.route("/register-branch/<hospital_id>", methods=["GET", "POST"])
def register_branch(hospital_id):
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

        save_branch(
            hospital_id=hospital_id,
            branch_name=branch_name,
            address=address,
            is_headquarters=is_headquarters,
            phone=phone or None,
            email=email or None,
            location=location or None,
            information=information or None,
        )

        return f"Branch '{branch_name}' registered successfully!"

    return render_template("register_branch.html", hospital_id=hospital_id)


if __name__ == "__main__":
    app.run(debug=True)
