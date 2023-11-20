from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages
from flask_mysqldb import MySQL
import os
import secrets

secret_key = secrets.token_hex(16)
print("this is secret key", secret_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# Load configuration from environment variables or a configuration file
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'Mahendra@1')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'sd1')

# Initialize MySQL extension
mysql = MySQL(app)

# Check MySQL connection within Flask application context
with app.app_context():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        print("MySQL connection successful!")
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        cursor.close()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = []  # Initialize messages variable

    if request.method == 'POST':
        # Handle the login logic for POST requests
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password match a registered user
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Successful login, set session variable and redirect to home page
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            # Invalid credentials, show error message
            flash('Username and password do not match. Please try again.', 'error')

    # Retrieve flashed messages and clear them
    messages = get_flashed_messages()

    return render_template('login.html', messages=messages)

@app.route('/index')
def index():
    # Your existing logic for the index page
    return render_template('index.html')


# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        flash(f'User {username} successfully registered! You can now log in.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
