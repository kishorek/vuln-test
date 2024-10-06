from flask import Flask, redirect, request, render_template, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """
    )
    conn.execute(
        """
        INSERT OR IGNORE INTO users (username, password) 
        VALUES ('admin', 'password123');
    """
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    return conn


# SQL Injection vulnerability
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Vulnerable query: No parameterization, allows SQL injection
        conn = get_db_connection()
        query = (
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        )
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            return redirect(url_for("greet"))
        else:
            message = "Invalid credentials!"
            return render_template("index.html", page="login", message=message)
    return render_template("index.html", page="login")


# XSS Vulnerability
@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        name = request.form["name"]

        # Vulnerable to XSS as input is directly rendered without sanitization
        message = f"Hello {name}"
        return render_template("index.html", page="greet", message=message)

    return render_template("index.html", page="greet")


if __name__ == "__main__":
    app.run(debug=True, port=9000, host="0.0.0.0")
