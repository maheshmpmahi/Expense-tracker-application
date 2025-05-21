from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "expense_tracker"

DATA_FILE = "expenses.json"  # Define the file path for storing expenses
USER_FILE = "users.json"

# Function to load expenses from JSON file
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):  
                    return data  
                elif isinstance(data, dict):  
                    return data.get("expenses", [])  
                else:  
                    return []  
            except json.JSONDecodeError:
                return []
    return []

# Function to save expenses to JSON file
def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump({"expenses": expenses}, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    # Redirect to login first if user is not authenticated
    if "user" not in session:
        return redirect(url_for("login"))

    expenses = load_expenses()
    error = None

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        amount = request.form.get("amount")

        # Validate input
        if not description:
            error = "Description cannot be empty."
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    error = "Amount must be positive."
            except ValueError:
                error = "Invalid amount. Please enter a valid number."

        if error:
            return render_template("index.html", expenses=expenses, error=error)

        timestamp = datetime.now().isoformat()

        # Assign a unique ID to each expense
        expense_id = len(expenses)  # Assign a unique ID based on list length

        expenses.append({
            "id": expense_id,  # Now every expense has an ID
            "timestamp": timestamp,
            "description": description,
            "amount": amount
        })
        save_expenses(expenses)

        return redirect(url_for("index"))

    return render_template("index.html", expenses=expenses, error=error)

@app.route("/view_expenses", methods=["GET", "POST"])
def view_expenses():
    """Displays the expense history and handles deleting expenses."""
    expenses = load_expenses()
    error = None

    if request.method == "POST" and "delete" in request.form:
        try:
            del_index = int(request.form.get("delete", -1))  # Default to invalid index if missing
            if 0 <= del_index < len(expenses):  # Validate index range
                expenses.pop(del_index)
                save_expenses(expenses)
                return redirect(url_for("view_expenses"))  # Redirect after successful deletion
            else:
                error = "Invalid expense index."
        except ValueError:
            error = "Invalid delete request. Please provide a valid expense index."

    return render_template("view_expenses.html", expenses=expenses, error=error, datetime=datetime)

@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e.get("id") != expense_id]  # Remove matching expense
    save_expenses(expenses)
    return redirect(url_for("view_expenses"))

@app.route("/summary")
def summarize_expenses():
    """Calculates and displays the total expenses."""
    expenses = load_expenses()
    total = sum(expense["amount"] for expense in expenses) if expenses else 0
    return render_template("summary.html", total=total)

# Load and Save Users Functions
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f).get("users", {})
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump({"users": users}, f, indent=4)

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Sign up successful! Please log in.")

    return render_template("login.html")

# Signup Route
@app.route("/signup", methods=["POST"])
def signup():
    users = load_users()
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if not username or not email or not password or not confirm_password:
        return render_template("login.html", error="All fields are required.")
    if password != confirm_password:
        return render_template("login.html", error="Passwords do not match.")
    if username in users:
        return render_template("login.html", error="Username already exists.")

    users[username] = password
    save_users(users)
    return redirect(url_for("login"))

# Dashboard Route (Protected Page)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
