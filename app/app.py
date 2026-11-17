import os
import time
from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "studentuser"),
        password=os.getenv("DB_PASSWORD", "studentpass"),
        database=os.getenv("DB_NAME", "studentdb")
    )

def initialize_database():
    for attempt in range(15):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    course VARCHAR(100) NOT NULL
                )
            """)
            connection.commit()
            cursor.close()
            connection.close()
            return
        except Error:
            time.sleep(2)
    raise RuntimeError("Could not connect to the MySQL database.")

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/", methods=["GET"])
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("index.html", students=students)
    except Error:
        return "Database is not available. Please try again.", 503

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()

    if name and email and course:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
            (name, email, course)
        )
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
