from flask import Flask, render_template, request, redirect, url_for, g
from helpers import error_message
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Flask configuration
app = Flask(__name__)

# Database configuration
DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        # Create tables for

    return db

# Function to initialize the database (run once to create the table)
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        with app.open_resource(resource='sql_scripts/users.sql',mode='r') as f:
            cursor.executescript(f.read())
        db.commit()  # Commit the changes to the database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Here, add code to handle registration (e.g., save to a database, validation)
                # Username checks
        if not username:
            return error_message("Must provide username")
        if not password or not confirm_password:
            return error_message('Must provide both password and confirmation')
        if password != confirm_password:
            return error_message('Password and confirmation must match')
        
        # Could implement a must characters for username and minimum length for password

        db = get_db()
        password_hash = generate_password_hash(password)
        try:
            # Use one cursor for both queries
            cursor = db.cursor()

            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                        (username, password_hash))
            
            # Commit the transaction
            db.commit()

            # Fetch and print all users to visualize the table
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()  # Fetch all rows

            # Print the users for debugging purposes
            for user in users:
                print(user)

            # Redirect to the login page after success
            return redirect('/login')

        except Exception as e:
            # Print the error for debugging purposes
            print(f"Error occurred: {e}")
            return error_message(str(e))  # Make sure e is converted to a string


    return render_template('identification.html', form_type='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        if not username or not password:
            return error_message('Must provide both username and password for the login')        
    return render_template('identification.html', form_type='login')

@app.route('/')
def home():
    
    return "TODO"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
