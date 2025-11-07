from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.permanent_session_lifetime = timedelta(days=7)

# ---------------------- MONGODB SETUP ----------------------
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_app"  # Change if needed
mongo = PyMongo(app)
users_collection = mongo.db.users
expenses_collection = mongo.db.expenses

# ---------------------- DEFAULT ROUTE ----------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------------- SIGNUP ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].lower()
        email = request.form['email'].lower()          # get email from form
        password = request.form['password']
        confirm = request.form['confirm_password']     # matches HTML name

        # Check if passwords match
        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        # Check if username already exists
        if users_collection.find_one({"username": username}):
            flash("Username already exists!", "warning")
            return redirect(url_for('signup'))

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            flash("Email already registered!", "warning")
            return redirect(url_for('signup'))

        # Hash password and save user
        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_pw
        })

        flash("Account created! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')


# ---------------------- LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # TODO: Send reset link email logic here
        flash('Password reset link has been sent to your email!', 'success')
        return redirect(url_for('login'))
    return render_template('forgot-password.html')

# ---------------------- LOGOUT ----------------------
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    flash("You have been logged out successfully!", "success")
    return redirect(url_for('login'))

# ---------------------- DASHBOARD ----------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))

    username = session['user']
    user_expenses = list(expenses_collection.find({"username": username}))
    total = sum(exp['amount'] for exp in user_expenses)
    return render_template('dashboard.html', username=username, expenses=user_expenses, total=total)

# ---------------------- ADD EXPENSE ----------------------
@app.route('/add', methods=['POST'])
def add_expense():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    title = request.form['title']
    amount = float(request.form['amount'])
    split_with = request.form['split_with'].split(',') if request.form['split_with'] else []
    each_share = round(amount / (len(split_with) + 1), 2)

    exp = {
        "username": username,
        "title": title,
        "amount": amount,
        "split_with": split_with,
        "each_share": each_share
    }

    expenses_collection.insert_one(exp)
    flash(f"Expense added! Each person pays ₹{each_share}", "success")
    return redirect(url_for('dashboard'))

# ---------------------- UPDATE EXPENSE ----------------------
@app.route('/update/<expense_id>', methods=['POST'])
def update_expense(expense_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    exp = expenses_collection.find_one({"_id": ObjectId(expense_id), "username": username})

    if exp:
        title = request.form['title']
        amount = float(request.form['amount'])
        split_with = request.form['split_with'].split(',') if request.form['split_with'] else []
        each_share = round(amount / (len(split_with) + 1), 2)

        expenses_collection.update_one(
            {"_id": ObjectId(expense_id)},
            {"$set": {
                "title": title,
                "amount": amount,
                "split_with": split_with,
                "each_share": each_share
            }}
        )

    flash("Expense updated successfully!", "info")
    return redirect(url_for('dashboard'))

# ---------------------- DELETE EXPENSE ----------------------
@app.route('/delete/<expense_id>')
def delete_expense(expense_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    expenses_collection.delete_one({"_id": ObjectId(expense_id), "username": username})
    flash("Expense deleted successfully!", "danger")
    return redirect(url_for('dashboard'))

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    app.run(debug=True)
