-- ============================================================
-- GuestSphere - MySQL Database Schema
-- Run this after creating the database, e.g.:
--   CREATE DATABASE guestsphere CHARACTER SET utf8mb4;
--   USE guestsphere;
--   SOURCE schema.sql;
-- Note: if you run `python init_db.py`, SQLAlchemy creates these
-- tables automatically from the models - this file is provided for
-- manual setup / documentation / academic submission purposes.
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'admin',
    is_active_flag BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    venue VARCHAR(200) NOT NULL,
    capacity INT NOT NULL DEFAULT 100,
    status VARCHAR(20) NOT NULL DEFAULT 'upcoming',
    created_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_events_date (event_date)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS guests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    gender VARCHAR(20),
    organization VARCHAR(150),
    rsvp_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    qr_token VARCHAR(64) NOT NULL UNIQUE,
    face_registered BOOLEAN DEFAULT FALSE,
    checkin_status BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    UNIQUE KEY uq_guest_event_email (event_id, email),
    INDEX idx_guests_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS invitations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    token VARCHAR(64) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'sent',
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    responded_at DATETIME,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS rsvps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    event_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    responded_at DATETIME,
    note VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    event_id INT NOT NULL,
    checkin_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(20) NOT NULL,
    confidence FLOAT,
    checked_in_by INT,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (checked_in_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS face_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    label_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS seating_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL DEFAULT 8,
    is_vip BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS seating_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    guest_id INT NOT NULL UNIQUE,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES seating_tables(id) ON DELETE CASCADE,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(150) NOT NULL,
    message VARCHAR(300) NOT NULL,
    category VARCHAR(30) DEFAULT 'general',
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;
