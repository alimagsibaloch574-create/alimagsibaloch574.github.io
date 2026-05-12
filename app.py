from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

accounts = {}

# LOGIN PAGE
@app.route('/')
def login():
    return render_template('login.html')

# LOGIN CHECK
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    if username == "admin" and password == "1234":
        session['user'] = username
        return redirect('/dashboard')
    else:
        return "❌ Invalid Login"

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', accounts=accounts)
    return redirect('/')

# CREATE ACCOUNT
@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name').strip()
    acc_no = request.form.get('acc_no').strip()

    if acc_no in accounts:
        return "⚠️ Account already exists"

    accounts[acc_no] = {"name": name, "balance": 0}
    return redirect('/dashboard')

# DEPOSIT (FIXED ✅)
@app.route('/deposit', methods=['POST'])
def deposit():
    acc_no = request.form.get('acc_no').strip()
    amount = request.form.get('amount')

    if acc_no not in accounts:
        return "❌ Account not found"

    try:
        amount = float(amount)
    except:
        return "❌ Invalid amount"

    accounts[acc_no]['balance'] += amount
    return redirect('/dashboard')

# WITHDRAW
@app.route('/withdraw', methods=['POST'])
def withdraw():
    acc_no = request.form.get('acc_no').strip()
    amount = request.form.get('amount')

    if acc_no not in accounts:
        return "❌ Account not found"

    try:
        amount = float(amount)
    except:
        return "❌ Invalid amount"

    if accounts[acc_no]['balance'] >= amount:
        accounts[acc_no]['balance'] -= amount

    return redirect('/dashboard')

# RUN
app.run(debug=True)