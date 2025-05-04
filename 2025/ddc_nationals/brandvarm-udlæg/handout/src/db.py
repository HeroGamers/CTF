import sqlite3
import hashlib
import uuid

# Database initialization
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT DEFAULT 'user')''')

    # Create expenses table with UUID
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id TEXT PRIMARY KEY,
                  user_id INTEGER,
                  title TEXT,
                  description TEXT,
                  amount REAL,
                  image_name TEXT,
                  status TEXT DEFAULT 'pending',
                  date_submitted TEXT,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper functions for database operations
def get_user_by_username(username):
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 (username, hashed_password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def add_expense(user_id, title, description, amount, image_name):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    expense_id = str(uuid.uuid4())
    c.execute("INSERT INTO expenses (id, user_id, title, description, amount, image_name, date_submitted) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
             (expense_id, user_id, title, description, amount, image_name))
    conn.commit()
    conn.close()
    return expense_id

def get_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = c.fetchone()
    conn.close()
    return expense

def get_expenses_by_user(user_id):
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date_submitted DESC", (user_id,))
    expenses = c.fetchall()
    conn.close()
    return expenses

def get_all_expenses():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT e.*, u.username FROM expenses e JOIN users u ON e.user_id = u.id ORDER BY date_submitted DESC")
    expenses = c.fetchall()
    conn.close()
    return expenses

def verify_password(stored_password, provided_password):
    hashed_provided = hash_password(provided_password)
    return stored_password == hashed_provided
