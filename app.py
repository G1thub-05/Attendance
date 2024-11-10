
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
import os

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# ========================= Database Connection Start =======================================================================
def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',         
            user='root',              
            password='Buggu@05',       
            database='Student'   
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
# ========================= Database Connection End ==========================================================================


# ======================================== Login Page Start ==================================================================

app.secret_key = os.urandom(24)  # For session handling, use a secure random key

@app.route('/')
def Login_Page():
    return render_template('Login_Page.html')

# Route to render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to check if the username and password match
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        # Close the database connection
        cursor.close()
        conn.close()

        # Check if user exists
        if user:
            # Log in successful, redirect to dashboard
            session['user_id'] = user['id']  # Store user ID in session (optional)
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials, flash a message
            flash("Invalid username or password", "error")
            flash("Please log in to access the dashboard", "info")
            return redirect(url_for('Login_Page'))

    return render_template('login.html')

# Dashboard route (accessible only after login)
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to access the dashboard", "warning")
        return redirect(url_for('login'))
    
    return redirect(url_for('Dash_Board'))  # Render dashboard page

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('Login_Page'))

# ======================================== Login Page End=====================================================================


# =================================Photo Upload Start=========================================================================
# Folder setup
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Default profile picture
DEFAULT_PROFILE_PIC = os.path.join(app.config['UPLOAD_FOLDER'], 'Profile.jpg')

@app.route('/Profile', methods=['GET', 'POST'])
def Profile_Page():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['photo']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            # Save the uploaded file
            filename = secure_filename("Your_Profile_Photo.jpg")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('Profile Photo Saved Successfully')
            return redirect(url_for('Profile_Page'))

    # Check if uploaded profile photo exists
    profile_pic = os.path.join(app.config['UPLOAD_FOLDER'], 'Your_Profile_Photo.jpg')
    if not os.path.isfile(profile_pic):
        profile_pic = DEFAULT_PROFILE_PIC

    return render_template('Profile_Page.html', profile_pic=profile_pic)
# =================================Photo Upload End===========================================================================



# =================================== Dash_Board & Mark_Attendance & View_Attendance Start ===================================
@app.route('/Dash_Board')
def Dash_Board():
    connection = get_db_connection()
    
    if not connection:
        return "Error connecting to the database."
    
    try:
        cursor = connection.cursor(dictionary=True)
        # Query to fetch student attendance details
        cursor.execute("SELECT id, name, class, semester, day, date, time, status FROM attendance")
        attendance_records = cursor.fetchall()
        cursor.execute("SELECT count(id) FROM attendance")
        total = cursor.fetchall()
    except Error as e:
        return f"An error occurred while fetching data: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # Check if uploaded profile photo exists
        DEFAULT_PROFILE_PIC = os.path.join(app.config['UPLOAD_FOLDER'], 'Profile.jpg')
        profile_pic = os.path.join(app.config['UPLOAD_FOLDER'], 'Your_Profile_Photo.jpg')
        if not os.path.isfile(profile_pic):
         profile_pic = DEFAULT_PROFILE_PIC
    # Render the View_Attendance with attendance data
    return render_template('dash_board.html', attendance=attendance_records, total=total, profile_pic=profile_pic)

@app.route('/Mark_Attendance')
def Mark_Attendance():
    connection = get_db_connection()
    if not connection:
        return "Error connecting to the database."
    try:
        DEFAULT_PROFILE_PIC = os.path.join(app.config['UPLOAD_FOLDER'], 'Profile.jpg')
        profile_pic = os.path.join(app.config['UPLOAD_FOLDER'], 'Your_Profile_Photo.jpg')
        if not os.path.isfile(profile_pic):
         profile_pic = DEFAULT_PROFILE_PIC
        cursor = connection.cursor(dictionary=True)
        # Query to fetch student attendance detail
        cursor.execute("SELECT id, name, class, semester, day, date, status FROM attendance where id = 7")
        attendance_records = cursor.fetchall()
    except Error as e:
        return f"An error occurred while fetching data: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Render the View_Attendance with attendance data
    return render_template('mark_attendance.html', attendance=attendance_records, profile_pic=profile_pic)

@app.route('/View_Attendance')
def View_Attendance():
    # Connect to the database and fetch student attendance data
    connection = get_db_connection()
    if not connection:
        return "Error connecting to the database."
    
    try:
        DEFAULT_PROFILE_PIC = os.path.join(app.config['UPLOAD_FOLDER'], 'Profile.jpg')
        profile_pic = os.path.join(app.config['UPLOAD_FOLDER'], 'Your_Profile_Photo.jpg')
        if not os.path.isfile(profile_pic):
         profile_pic = DEFAULT_PROFILE_PIC
        cursor = connection.cursor(dictionary=True)
        # Query to fetch student attendance details
        cursor.execute("SELECT id, name, class, semester, day, date, status FROM attendance where id = 7")
        attendance_records = cursor.fetchall()
    except Error as e:
        return f"An error occurred while fetching data: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 

    # Render the View_Attendance with attendance data
    return render_template('view_attendance.html', attendance=attendance_records, profile_pic=profile_pic)
# =================================== Dash_Board & Mark_Attendance & View_Attendance End ===================================


if __name__ == '__main__': 
    app.run(debug=True)
