from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages
import mysql.connector
import os
import secrets

secret_key = secrets.token_hex(16)
print("this is the secret key", secret_key)
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# Load configuration from environment variables or a configuration file
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'Mahendra@1')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'sd1')

# Initialize MySQL connection
# Check if the username and password match a registered user
connection = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    auth_plugin='mysql_native_password'
)
cursor = connection.cursor(dictionary=True)



@app.route('/')
def landing():
    if 'logged_in' in session and session['logged_in']:
        print("User is logged in. Redirecting to index page.")
        return redirect(url_for('index'))
    else:
        print("User is not logged in. Rendering landing.html.")
        return render_template('landing.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = []  # Initialize messages variable

    if request.method == 'POST':
        try:
            # Handle the login logic for POST requests
            username = request.form.get('username')
            password = request.form.get('password')

            print(f"Attempting login with username: {username} and password: {password}")

            # Check if the username and password match a registered user
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            # Clear any unread results
            cursor.fetchall()

            if user:
                # Successful login, set session variable and redirect to home page
                print(f"Login successful for user: {user}")
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                # Invalid credentials, show error message
                print("Invalid credentials.")
                flash('Username and password do not match. Please try again.', 'error')
        except mysql.connector.Error as sql_error:
            print(f"MySQL Error during login: {sql_error}")
            flash('Usernmae OR Password  Wrong Please Check And try again.', 'error')
        except Exception as e:
            print(f"Unexpected error during login: {e}")
            flash('An unexpected error occurred. Please try again.', 'error')

    # Retrieve flashed messages and clear them
    messages = get_flashed_messages()

    print("Flashed Messages:", messages)

    return render_template('login.html', messages=messages)












# Index Page

@app.route('/index')
def index():
    # Check if the user is logged in
    if 'logged_in' in session and session['logged_in']:
        print("User is logged in. Rendering index.html.")
        return render_template('index.html')
    else:
        # If not logged in, redirect to the login page
        print("User is not logged in. Redirecting to login page.")
        flash('Please log in to access the index page.', 'error')
        return redirect(url_for('login'))


# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic
        # ...

        return redirect(url_for('login'))  # Redirect to the login page after registration

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    print("Session cleared. Redirecting to login.")
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
