from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify
from flask_session import Session
from helpers import error_message, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Flask configuration
app = Flask(__name__)
 # Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)   

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# Database configuration
DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
       

    return db

# Function to initialize the database (run once to create the table)
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        with app.open_resource(resource='sql_scripts/users.sql',mode='r') as f:
            cursor.executescript(f.read())
        db.commit()  # Commit the changes to the database
        
        with app.open_resource(resource='sql_scripts/tickets.sql',mode='r') as t:
            cursor.executescript(t.read())            
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
        
            cursor = db.cursor()
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                        (username, password_hash))
            
            db.commit()

            cursor.execute('SELECT * FROM users')


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
        db = get_db()
        cursor = db.cursor()
        users_data = cursor.execute('SELECT * FROM users where username = ?', (username,))
        user = users_data.fetchone()
        if not user:
            return error_message("The inserted user does not exist or the password does not match the user's password.")      
        stored_hash_pwd = user['password']

        if not check_password_hash(pwhash=stored_hash_pwd,password=password):
            return error_message("The inserted user does not exist or the password does not match the user's password.")

        session['user_id'] = user['id']
        session['username'] = user['username']
        # session.permanent = False
        return redirect('/main')

    return render_template('identification.html', form_type='login')

@app.route('/')
@login_required
def home():
    
    return redirect('/main')

@app.route('/main')
@login_required
def main():
    if request.method == 'GET':
        tickets = []
        try:
            db = get_db()
            cursor = db.cursor()
            
            user_tickets = cursor.execute('SELECT * FROM tickets WHERE user_id = ? and is_deleted = 0 and is_archived = 0 ORDER BY due_date ASC ', (1,))

            tickets = user_tickets.fetchall()

        except Exception as e:
            print(e)
            return error_message(e)
        return render_template('main.html', username=session['username'], tickets=tickets)
    return "TODO"



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route('/create_ticket', methods=['POST'])
@login_required
def create_ticket():
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO tickets (user_id, title, description, due_date, is_deleted) VALUES (?,?,?,?,?)',(session['user_id'], title, description, due_date, 0))

        db.commit()
    except Exception as e:
        return error_message(e)
    # Return the new ticket data as a JSON response
    return jsonify({
        'id': 1,
        'title': title,
        'description': description,
        'due_date': due_date
    })


@app.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    db = get_db()  # Connect to your database
    cursor = db.cursor()

    # Fetch the specific ticket from the database
    ticket = cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()

    if request.method == 'POST':
        # Handle the form submission to update the ticket
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        archive = request.form.get('archive')
        is_archived = 1 if archive else 0

        # Update the ticket in the database
        cursor.execute('UPDATE tickets SET title = ?, description = ?, due_date = ?, is_archived = ? WHERE id = ?',
                       (title, description, due_date, is_archived, ticket_id))
        db.commit()

        return redirect(url_for('main'))  # Redirect back to the dashboard

    return render_template('edit_ticket.html', ticket=ticket)


@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute('UPDATE tickets SET is_deleted = 1 WHERE id = ?', (ticket_id,))
        db.commit()
        return redirect(url_for('main'))  # Redirect back to the main page
    except Exception as e:
        return error_message(e)
    
@app.route('/permanently_delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def permanently_delete_ticket(ticket_id):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute('DELETE from tickets WHERE id = ?', (ticket_id,))
        db.commit()
        return redirect(url_for('main'))  # Redirect back to the main page
    except Exception as e:
        return error_message(e)    
    
@app.route('/ticket_history')
@login_required
def ticket_history():
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Fetch all tickets for the logged-in user
        tickets = cursor.execute('SELECT * FROM tickets WHERE user_id = ?', (session['user_id'],)).fetchall()
    except Exception as e:
        return error_message(str(e))
    
    return render_template('ticket_history.html', tickets=tickets)




if __name__ == '__main__':
    init_db()
    session.clear()
    app.run(debug=True)
