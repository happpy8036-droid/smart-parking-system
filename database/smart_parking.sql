-- ============================================================
-- Smart Parking System — Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart_parking_db;
USE smart_parking_db;

-- ─── Users Table ───
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'premium') DEFAULT 'user',
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Admins Table ───
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'super_admin') DEFAULT 'admin',
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Vehicles Table ───
CREATE TABLE vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL,
    vehicle_type ENUM('car', 'bike', 'suv', 'truck', 'ev') DEFAULT 'car',
    color VARCHAR(50),
    brand VARCHAR(100),
    is_default TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Parking Areas Table ───
CREATE TABLE parking_areas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    area VARCHAR(100),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    price_per_hour DECIMAL(8, 2) NOT NULL DEFAULT 50.00,
    open_time VARCHAR(10) NOT NULL DEFAULT '00:00',
    close_time VARCHAR(10) NOT NULL DEFAULT '23:59',
    total_slots INT NOT NULL DEFAULT 0,
    available_slots INT NOT NULL DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Parking Slots Table ───
CREATE TABLE parking_slots (
    id INT PRIMARY KEY AUTO_INCREMENT,
    area_id INT NOT NULL,
    slot_number VARCHAR(50) NOT NULL,
    slot_type ENUM('standard', 'premium', 'ev_charging', 'handicap', 'bike') DEFAULT 'standard',
    status ENUM('available', 'occupied', 'reserved', 'maintenance') DEFAULT 'available',
    price_per_hour DECIMAL(8, 2) NOT NULL DEFAULT 50.00,
    is_special TINYINT(1) DEFAULT 0,
    `row` VARCHAR(10),
    `col` INT,
    floor INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (area_id) REFERENCES parking_areas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Bookings Table ───
CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    slot_id INT NOT NULL,
    area_id INT NOT NULL,
    vehicle_id INT,
    booking_date VARCHAR(20) NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) NOT NULL,
    duration INT NOT NULL COMMENT 'Duration in minutes',
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('confirmed', 'completed', 'cancelled', 'no_show') DEFAULT 'confirmed',
    booking_ref VARCHAR(20) NOT NULL UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (slot_id) REFERENCES parking_slots(id),
    FOREIGN KEY (area_id) REFERENCES parking_areas(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Payments Table ───
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('card', 'upi', 'netbanking', 'wallet', 'cash') DEFAULT 'card',
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    receipt_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Notifications Table ───
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read TINYINT(1) DEFAULT 0,
    notification_type ENUM('booking', 'payment', 'system', 'promotion') DEFAULT 'system',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Feedback Table ───
CREATE TABLE feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    booking_id INT,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Activity Log Table ───
CREATE TABLE activity_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── Indexes for Performance ───
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_date ON bookings(booking_date);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_slots_area ON parking_slots(area_id);
CREATE INDEX idx_slots_status ON parking_slots(status);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_payments_booking ON payments(booking_id);
