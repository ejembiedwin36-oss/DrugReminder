from flask import Flask, render_template, request

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

        save_hospital(
            hospital_name=hospital_name,
            hospital_type=hospital_type,
            phone=phone,
            email=email,
            address=address,
        )

        return f"Hospital '{hospital_name}' registered successfully!"

    return render_template("register_hospital.html")


if __name__ == "__main__":
    app.run(debug=True)
