from flask import Flask, request, jsonify, render_template
from database import conn, cursor

# Create the Flask application
app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Employees endpoint
@app.route("/employees", methods=["GET", "POST"])
def manage_employees():

    if request.method == "GET":
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        return jsonify(employees)

    elif request.method == "POST":
        data = request.json

        name = data["name"]
        start_date = data["start_date"]
        location = data["location"]
        role = data["role"]

        cursor.execute(
            """
            INSERT INTO employees
            (name, start_date, location, role)
            VALUES (?, ?, ?, ?)
            """,
            (name, start_date, location, role)
        )

        conn.commit()

        return "Employee added successfully", 201


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
