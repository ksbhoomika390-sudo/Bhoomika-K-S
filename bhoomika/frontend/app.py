from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        return f"Registered Successfully! Name: {name}, Email: {email}"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        return f"Login Successful! Email: {email}"
    return render_template("login.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = request.form.get("message")
        return f"Message Received: {message}"
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)