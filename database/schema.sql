-- College Event Management System Database Schema

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS college_events;
USE college_events;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50) NOT NULL,
    batch VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    venue VARCHAR(200) NOT NULL,
    department VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_department (department),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Registrations table (junction table for students and events)
CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (student_id, event_id),
    INDEX idx_student (student_id),
    INDEX idx_event (event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample events
INSERT INTO events (title, description, date, venue, department) VALUES
(
    'Tech Symposium 2025',
    'Annual technical symposium featuring coding competitions, hackathons, and tech talks. Join us for a day filled with innovation, learning, and networking opportunities. Prizes worth ₹50,000 to be won!',
    '2025-11-15 09:00:00',
    'Main Auditorium',
    'CSE'
),
(
    'Circuit Design Workshop',
    'Hands-on workshop on PCB design and circuit simulation using industry-standard tools. Learn from experts and get practical experience in circuit design and troubleshooting.',
    '2025-11-20 14:00:00',
    'ECE Lab Block',
    'ECE'
),
(
    'Robotics Competition',
    'Build and compete with your autonomous robots. Show off your engineering skills and creativity. Categories include line following, maze solving, and combat robots.',
    '2025-12-01 10:00:00',
    'Sports Complex',
    'EEE'
),
(
    'CAD Modeling Contest',
    'Showcase your 3D modeling and design skills using AutoCAD and SolidWorks. Create innovative solutions for real-world mechanical engineering challenges.',
    '2025-11-25 11:00:00',
    'MECH Workshop',
    'MECH'
),
(
    'Structural Design Expo',
    'Exhibition of innovative structural designs and models. Present your ideas for sustainable and efficient building designs. Special focus on earthquake-resistant structures.',
    '2025-12-05 09:30:00',
    'CIVIL Department',
    'CIVIL'
),
(
    'AI/ML Bootcamp',
    'Intensive bootcamp on Artificial Intelligence and Machine Learning. Topics include deep learning, computer vision, and natural language processing. Bring your laptops!',
    '2025-11-18 10:00:00',
    'Computer Lab 1',
    'CSE'
),
(
    'Cultural Fest 2025',
    'Inter-department cultural festival with music, dance, and drama competitions. Celebrate the diversity of talents in our college. Food stalls and fun activities throughout the day.',
    '2025-12-10 16:00:00',
    'Open Air Theatre',
    'All Departments'
);

-- Create admin table (for fixed admin credentials)
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default admin account (username: admin, password: admin123)
-- Note: In production, use a strong password and change these credentials
INSERT INTO admins (username, password) VALUES 
('admin', 'pbkdf2:sha256:600000$dR6RicSHoNXKxSxk$7d04ac668e17146ce35c6c05a532bb2bb7365b78f0e07d64690f96c0f7c5f5b0');
