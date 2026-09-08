from flask import Flask, render_template, request

app = Flask(__name__)

#hello
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
        return hospital_name

    else:
        return render_template("register_hospital.html")

    

if __name__ == "__main__":
        app.run(debug=True)
