from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import csv
import io
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change this
    'database': 'college_events'
}

# Database connection helper
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin login required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Student Signup
@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        batch = request.form['batch']
        password = request.form['password']
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (name, email, department, batch, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, department, batch, hashed_password)
                )
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('student_login'))
            except Error as e:
                flash(f'Registration failed: Email already exists or invalid data.', 'danger')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('student_signup.html')

# Student Login
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
                student = cursor.fetchone()
                
                if student and check_password_hash(student['password'], password):
                    session['student_id'] = student['id']
                    session['student_name'] = student['name']
                    session['student_department'] = student['department']
                    flash(f'Welcome back, {student["name"]}!', 'success')
                    return redirect(url_for('student_dashboard'))
                else:
                    flash('Invalid email or password.', 'danger')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('student_login.html')

# Student Dashboard
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    department_filter = request.args.get('department', 'All Departments')
    
    conn = get_db_connection()
    events = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if department_filter == 'All Departments':
                cursor.execute("SELECT * FROM events ORDER BY date ASC")
            else:
                cursor.execute("SELECT * FROM events WHERE department = %s OR department = 'All Departments' ORDER BY date ASC", (department_filter,))
            events = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    return render_template('student_dashboard.html', events=events, current_filter=department_filter)

# Event Details
@app.route('/event/<int:event_id>')
@login_required
def event_details(event_id):
    conn = get_db_connection()
    event = None
    is_registered = False
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
            
            # Check if student is already registered
            cursor.execute(
                "SELECT * FROM registrations WHERE student_id = %s AND event_id = %s",
                (session['student_id'], event_id)
            )
            is_registered = cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()
    
    return render_template('event_details.html', event=event, is_registered=is_registered)

# Register for Event
@app.route('/event/<int:event_id>/register', methods=['POST'])
@login_required
def register_event(event_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO registrations (student_id, event_id) VALUES (%s, %s)",
                (session['student_id'], event_id)
            )
            conn.commit()
            flash('Successfully registered for the event!', 'success')
        except Error as e:
            flash('You are already registered for this event.', 'warning')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('event_details', event_id=event_id))

# My Registrations
@app.route('/student/registrations')
@login_required
def my_registrations():
    conn = get_db_connection()
    registrations = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT e.*, r.timestamp 
                FROM events e 
                JOIN registrations r ON e.id = r.event_id 
                WHERE r.student_id = %s 
                ORDER BY r.timestamp DESC
            """, (session['student_id'],))
            registrations = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    return render_template('my_registrations.html', registrations=registrations)

# Student Logout
@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    session.pop('student_name', None)
    session.pop('student_department', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Fixed admin credentials (username: admin, password: admin123)
        if username == 'admin' and password == 'admin123':
            session['admin_id'] = 1
            session['admin_username'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
    
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    events = []
    total_events = 0
    total_registrations = 0
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM events ORDER BY date DESC")
            events = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) as count FROM events")
            total_events = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM registrations")
            total_registrations = cursor.fetchone()['count']
        finally:
            cursor.close()
            conn.close()
    
    return render_template('admin_dashboard.html', events=events, total_events=total_events, total_registrations=total_registrations)

# Add Event
@app.route('/admin/event/add', methods=['GET', 'POST'])
@admin_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        venue = request.form['venue']
        department = request.form['department']
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO events (title, description, date, venue, department) VALUES (%s, %s, %s, %s, %s)",
                    (title, description, date, venue, department)
                )
                conn.commit()
                flash('Event added successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            finally:
                cursor.close()
                conn.close()
    
    return render_template('add_event.html')

# Edit Event
@app.route('/admin/event/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    conn = get_db_connection()
    event = None
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        venue = request.form['venue']
        department = request.form['department']
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE events SET title=%s, description=%s, date=%s, venue=%s, department=%s WHERE id=%s",
                    (title, description, date, venue, department, event_id)
                )
                conn.commit()
                flash('Event updated successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            finally:
                cursor.close()
                conn.close()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    
    return render_template('edit_event.html', event=event)

# Delete Event
@app.route('/admin/event/<int:event_id>/delete', methods=['POST'])
@admin_required
def delete_event(event_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
            conn.commit()
            flash('Event deleted successfully!', 'success')
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_dashboard'))

# View Event Registrations
@app.route('/admin/event/<int:event_id>/registrations')
@admin_required
def event_registrations(event_id):
    conn = get_db_connection()
    event = None
    registrations = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
            
            cursor.execute("""
                SELECT s.name, s.email, s.department, s.batch, r.timestamp 
                FROM students s 
                JOIN registrations r ON s.id = r.student_id 
                WHERE r.event_id = %s 
                ORDER BY r.timestamp DESC
            """, (event_id,))
            registrations = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    return render_template('event_registrations.html', event=event, registrations=registrations)

# Download Registrations CSV
@app.route('/admin/event/<int:event_id>/download')
@admin_required
def download_registrations(event_id):
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT title FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
            
            cursor.execute("""
                SELECT s.name, s.email, s.department, s.batch, r.timestamp 
                FROM students s 
                JOIN registrations r ON s.id = r.student_id 
                WHERE r.event_id = %s 
                ORDER BY r.timestamp DESC
            """, (event_id,))
            registrations = cursor.fetchall()
            
            # Create CSV
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Name', 'Email', 'Department', 'Batch', 'Registration Time'])
            
            for reg in registrations:
                writer.writerow([reg['name'], reg['email'], reg['department'], reg['batch'], reg['timestamp']])
            
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'{event["title"]}_registrations.csv'
            )
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
