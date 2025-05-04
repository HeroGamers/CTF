from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
import os
import uuid
from werkzeug.utils import secure_filename
import bot
from db import init_db, get_user_by_username, add_user, add_expense, get_expenses_by_user, get_expense, verify_password
import html
 
app = Flask(__name__) 
app.secret_key = os.urandom(24)

# No funny business with external scripts, or something idk... its just what the appsec guy told us. 
@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self' 127.0.0.1:* localhost:*; script-src 'unsafe-inline' 'unsafe-eval' 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' 127.0.0.1:* localhost:*;"
    return response

  
UPLOAD_FOLDER = 'static/receipts'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

if not os.path.exists('expenses.db'):
    init_db()

def require_login(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return wrapped

def require_logout(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrapped
 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html') 

@app.route('/login')
@require_logout
def login_page():
    return render_template('login.html')

@app.route('/register')
@require_logout
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
@require_login
def dashboard():
    expenses = get_expenses_by_user(session['user_id'])
    return render_template('dashboard.html', expenses=expenses, user=session['username'])

@app.route('/expense/new')
@require_login
def new_expense():
    return render_template('new_expense.html')

@app.route('/expense/<expense_id>')
def view_expense(expense_id):
    expense = get_expense(expense_id)
    if not expense:
        return render_template('404.html'), 404
    return render_template('view_expense.html', expense=expense)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Invalid credentials'}), 401

    user = get_user_by_username(username)

    if user and verify_password(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for("dashboard"))  
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username')

    if username and len(username) > 60:
        return jsonify({'error': 'Username cannot exceed 60 characters'}), 400
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing Information'}), 400

    if get_user_by_username(username):
        return jsonify({'error': 'Username already taken'}), 400

    if add_user(username, password):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/expenses', methods=['GET'])
@require_login
def get_user_expenses():
    expenses = get_expenses_by_user(session['user_id'])
    return jsonify({'expenses': [dict(expense) for expense in expenses]})

@app.route('/api/expenses', methods=['POST'])
@require_login
def create_expense():
    if 'receipt' not in request.files:
        return jsonify({'error': 'No receipt file'}), 400

    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return jsonify({'error': 'Only JPG and PNG files are allowed'}), 400

    filename = secure_filename(f"{uuid.uuid4()}_{html.escape(file.filename)}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    title = request.form.get('title')
    description = request.form.get('description')
    amount = request.form.get('amount')

    if not title or not amount:
        return jsonify({'error': 'Missing required fields'}), 400

    expense_id = add_expense(session['user_id'], html.escape(title), html.escape(description), html.escape(amount), html.escape(filename))

    return redirect(url_for('view_expense', expense_id=expense_id))


@app.route('/api/notify-admin', methods=['POST'])
@require_login
def notify_admin():
    expense_location = request.form.get('expense_location')

    if not expense_location:
        return jsonify({'error': 'No expense specified'}), 400

    success = bot.review_expense(expense_location)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to notify admin'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
