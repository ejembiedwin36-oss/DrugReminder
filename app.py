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
        hospital_name = request.form["hospital_name"]
        hospital_type = request.form["hospital_type"]
        phone = request.form["phone_number"]
        email = request.form["email"]
        address = request.form["address"]

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
