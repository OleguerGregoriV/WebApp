from flask import Flask, render_template, request, redirect, url_for
from helpers import error_message
app = Flask(__name__)

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
        return redirect(url_for('home'))
    
    return render_template('register.html', form_type='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('register.html', form_type='login')

@app.route('/')
def home():
    
    return "Welcome to your Task Management App!"

if __name__ == '__main__':
    app.run(debug=True)
