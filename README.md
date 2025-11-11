# 🎓 College Event Management System

A comprehensive web application for managing college events with separate portals for students and administrators.

## 📋 Features

### 👩‍🎓 Student Portal
- **User Registration & Authentication**
  - Sign up with college email, department, and batch
  - Secure login with password hashing
  - Session management

- **Event Management**
  - Browse all college events
  - Filter events by department (CSE, ECE, EEE, MECH, CIVIL, etc.)
  - View detailed event information
  - Register for events with one click
  - Track registered events in "My Registrations"

### 🧑‍💼 Admin Portal
- **Event Management**
  - Add new events with title, description, date, venue, and department
  - Edit existing events
  - Delete events
  - View all events in a dashboard

- **Registration Tracking**
  - View all student registrations for each event
  - Download registration lists as CSV files
  - See total events and registrations statistics

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Authentication**: Flask Sessions with Werkzeug password hashing

## 📁 Project Structure

```
college_event_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── database/
│   └── schema.sql             # Database schema and sample data
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── main.js            # JavaScript functionality
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── student_signup.html    # Student registration
    ├── student_login.html     # Student login
    ├── student_dashboard.html # Student event listing
    ├── event_details.html     # Event details page
    ├── my_registrations.html  # Student's registered events
    ├── admin_login.html       # Admin login
    ├── admin_dashboard.html   # Admin dashboard
    ├── add_event.html         # Add new event
    ├── edit_event.html        # Edit event
    └── event_registrations.html # View event registrations
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd college_event_system
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

1. **Start MySQL Server**
   ```bash
   # On Linux/Mac
   sudo service mysql start
   
   # On Windows
   # Start MySQL from Services or MySQL Workbench
   ```

2. **Create Database and Tables**
   ```bash
   mysql -u root -p < database/schema.sql
   ```
   
   Or manually in MySQL:
   ```sql
   mysql -u root -p
   ```
   Then copy and paste the contents of `database/schema.sql`

3. **Update Database Configuration**
   
   Edit `app.py` and update the database credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',              # Your MySQL username
       'password': 'your_password',  # Your MySQL password
       'database': 'college_events'
   }
   ```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🔐 Default Credentials

### Admin Login
- **Username**: `admin`
- **Password**: `admin123`

### Student Account
Students need to sign up first. No default student account is provided.

## 📊 Database Schema

### Tables

1. **students**
   - id (Primary Key)
   - name
   - email (Unique)
   - department
   - batch
   - password (Hashed)
   - created_at

2. **events**
   - id (Primary Key)
   - title
   - description
   - date
   - venue
   - department
   - created_at

3. **registrations**
   - id (Primary Key)
   - student_id (Foreign Key → students.id)
   - event_id (Foreign Key → events.id)
   - timestamp
   - Unique constraint on (student_id, event_id)

## 🎨 Features Breakdown

### Student Features
1. **Sign Up**: Create account with college email, department, and batch
2. **Login**: Secure authentication with session management
3. **Browse Events**: View all events or filter by department
4. **Event Details**: See complete information about any event
5. **Register**: One-click registration for events
6. **My Registrations**: Track all registered events
7. **Logout**: Secure session termination

### Admin Features
1. **Login**: Fixed admin credentials
2. **Dashboard**: Overview with statistics (total events, registrations)
3. **Add Event**: Create new events with all details
4. **Edit Event**: Modify existing event information
5. **Delete Event**: Remove events (with confirmation)
6. **View Registrations**: See all students registered for each event
7. **Download CSV**: Export registration lists for offline use
8. **Logout**: Secure session termination

## 🎯 Usage Guide

### For Students

1. **First Time Users**
   - Click "Student Sign Up" on the home page
   - Fill in your details (name, college email, department, batch, password)
   - Click "Sign Up"

2. **Returning Users**
   - Click "Student Login"
   - Enter your email and password
   - Click "Login"

3. **Browsing Events**
   - After login, you'll see all available events
   - Use the department filter to view specific department events
   - Click on any event card to view full details

4. **Registering for Events**
   - Click "View Details" on an event
   - Click "Register for Event" button
   - You'll see a confirmation message

5. **Viewing Your Registrations**
   - Click "My Registrations" in the navigation
   - See all events you've registered for

### For Admins

1. **Login**
   - Click "Admin Login"
   - Enter username: `admin`, password: `admin123`

2. **Adding Events**
   - Click "+ Add New Event" button
   - Fill in event details
   - Click "Add Event"

3. **Managing Events**
   - View all events in the dashboard
   - Click "Edit" to modify an event
   - Click "Delete" to remove an event (with confirmation)

4. **Viewing Registrations**
   - Click "View Registrations" for any event
   - See list of all registered students
   - Click "Download CSV" to export the list

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- SQL injection prevention with parameterized queries
- CSRF protection through Flask sessions
- Login required decorators for protected routes
- Unique email constraint for students
- Unique registration constraint (one student per event)

## 🎨 Design Features

- Modern gradient background
- Responsive design (mobile-friendly)
- Smooth animations and transitions
- Card-based event display
- Color-coded flash messages
- Hover effects on interactive elements
- Clean and intuitive navigation

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check database credentials in `app.py`
- Ensure `college_events` database exists

### Import Error
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

### Flash Messages Not Showing
- Clear browser cache
- Check if JavaScript is enabled

## 📝 Sample Data

The database schema includes sample events:
- Tech Symposium 2025 (CSE)
- Circuit Design Workshop (ECE)
- Robotics Competition (EEE)
- CAD Modeling Contest (MECH)
- Structural Design Expo (CIVIL)
- AI/ML Bootcamp (CSE)
- Cultural Fest 2025 (All Departments)

## 🚀 Deployment Options

### Local Development
Already covered in the setup instructions above.

### Production Deployment
For production deployment, consider:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set `debug=False` in `app.py`
3. Use environment variables for sensitive data
4. Enable HTTPS
5. Use a production-grade database setup
6. Implement proper logging

## 📄 License

This project is created for educational purposes.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Verify database setup

## 🎉 Enjoy!

Your College Event Management System is now ready to use. Students can browse and register for events, while admins can efficiently manage events and track registrations!
