from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = "supersecretkey"
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                password TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                role TEXT,
                salary TEXT)""")
    conn.commit()
    conn.close()
@app.route("/")
def home():
    return redirect(url_for("login"))
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                    (name, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?",
                    (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session["user"] = user[1]  
            return redirect(url_for("dashboard"))
        else:
            return "❌ Invalid email or password"
    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect(url_for("login"))
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        salary = request.form["salary"]
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO employees(name,role,salary) VALUES(?,?,?)",
                    (name, role, salary))
        conn.commit()
        conn.close()
        return redirect(url_for("view_employee"))
    return render_template("add_emp.html")
@app.route("/view")
def view_employee():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    conn.close()
    return render_template("view_emp.html", employees=data)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if request.method == "POST":
        cur.execute("""UPDATE employees
                    SET name=?, role=?, salary=?
                    WHERE id=?""",
                    (request.form["name"],
                     request.form["role"],
                     request.form["salary"], id))
        conn.commit()
        conn.close()
        return redirect(url_for("view_employee"))
    cur.execute("SELECT * FROM employees WHERE id=?", (id,))
    emp = cur.fetchone()
    conn.close()
    return render_template("edit_emp.html", emp=emp)
@app.route("/delete/<int:id>")
def delete_employee(id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_employee"))
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    init_db()
    app.run(debug=True)