from flask import Flask, render_template, request, redirect, session
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("users.db")

conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    password TEXT
)
""")
conn.commit()
conn.close()

# ---------- PASSWORD CHECK ----------
def strong_password(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*]", password):
        return False
    return True

# ---------- SIGNUP ----------
@app.route("/", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        first = request.form["first"]
        last = request.form["last"]
        raw_password = request.form["password"]

        if not strong_password(raw_password):
            error = "❌ Password must be strong (Upper, Lower, Number, Special, Min 8)"
            return render_template("signup.html", error=error)

        password = generate_password_hash(raw_password)

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users(email,username,first_name,last_name,password) VALUES(?,?,?,?,?)",
                (email, username, first, last, password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")

        except:
            error = "❌ Username already exists"
            return render_template("signup.html", error=error)

    return render_template("signup.html")
# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user[5], password):
            session["user"] = user[3]  # first name
            return redirect("/home")
        else:
            error = "❌ Invalid username or password"

    return render_template("login.html", error=error)

# ---------- HOME ----------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html", name=session["user"])

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)