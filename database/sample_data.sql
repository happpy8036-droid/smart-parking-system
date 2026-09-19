-- ============================================================
-- Smart Parking System — Sample Demo Data
-- ============================================================
USE smart_parking_db;

-- ─── Admin ───
INSERT INTO admins (name, email, password, role) VALUES
('Admin', 'admin@smartparking.com', 'scrypt:32768:8:1$TIvScrye35uoQYg5$ec5f475179a037355293dd2bd0c330be52c8c3485a5701d69a46d6e7621d3ad4804fae4af104cff87db8ac5a80733c7362b8149df9f0943d5cfa5f277faad64e', 'admin');

-- ─── Demo User ───
INSERT INTO users (name, email, phone, password, role) VALUES
('Rahul Sharma', 'rahul@example.com', '9876543210', 'scrypt:32768:8:1$XlPPNM9s34ZbzRRv$fee14089d5b625fc480e011a1edaa98dcf08f7514d6d62d28da1a1f68604292f72007935f5bdfa21f0ea290183926658a23fcb653ea036f8f4622f699c64458c', 'user'),
('Priya Patel', 'priya@example.com', '9876543211', 'scrypt:32768:8:1$XlPPNM9s34ZbzRRv$fee14089d5b625fc480e011a1edaa98dcf08f7514d6d62d28da1a1f68604292f72007935f5bdfa21f0ea290183926658a23fcb653ea036f8f4622f699c64458c', 'user');

-- ─── Vehicles ───
INSERT INTO vehicles (user_id, vehicle_number, vehicle_type, color, brand) VALUES
(1, 'AP16AB1234', 'car', 'White', 'Honda City'),
(1, 'AP16CD5678', 'bike', 'Black', 'Royal Enfield'),
(2, 'AP16EF9012', 'car', 'Red', 'Hyundai i20');

-- ─── Parking Areas ───
INSERT INTO parking_areas (name, address, city, area, latitude, longitude, price_per_hour, open_time, close_time, total_slots, available_slots, description) VALUES
('Uravali Theater Parking', 'Uravali, Inaspet, Rajahmundry', 'Rajahmundry', 'Uravali', 17.0005, 81.7825, 50.00, '06:00', '23:00', 80, 80, 'Parking at Uravali Theater area - convenient for moviegoers and shoppers'),
('Inorbit Mall Parking', 'Dantuluru, Rajahmundry', 'Rajahmundry', 'Dantuluru', 17.0150, 81.7900, 60.00, '10:00', '22:00', 150, 150, 'Multi-level parking at Inorbit Mall - shopping and dining destination'),
('Raja Cine Hall Parking', 'Danavaipet, Rajahmundry', 'Rajahmundry', 'Danavaipet', 17.0115, 81.7850, 40.00, '09:00', '23:30', 60, 60, 'Parking near Raja Cine Hall - popular cinema and entertainment hub'),
('Rajahmundry Bus Stand Parking', 'Near New Bus Stand, Kovvuru Road', 'Rajahmundry', 'Kovvuru Road', 17.0050, 81.7900, 30.00, '00:00', '23:59', 100, 100, 'Public parking near New Bus Stand - for commuters and travelers'),
('Godavari Bridge Parking', 'Near Havelock Bridge, Godavari', 'Rajahmundry', 'Godavari Bank', 17.0200, 81.7750, 45.00, '06:00', '22:00', 50, 50, 'Scenic parking near the iconic Godavari Bridge - tourist spot'),
('Apollo Hospital Parking', 'Rajendra Nagar, Rajahmundry', 'Rajahmundry', 'Rajendra Nagar', 17.0080, 81.7880, 55.00, '00:00', '23:59', 120, 120, 'Dedicated parking at Apollo Hospital campus - 24/7 available');

-- ─── Parking Slots (Sample for Area 1 — Uravali Theater) ───
INSERT INTO parking_slots (area_id, slot_number, slot_type, status, price_per_hour, `row`, `col`, floor) VALUES
(1, 'A-1', 'standard', 'available', 50.00, 'A', 1, 0),
(1, 'A-2', 'standard', 'available', 50.00, 'A', 2, 0),
(1, 'A-3', 'standard', 'available', 50.00, 'A', 3, 0),
(1, 'A-4', 'standard', 'available', 50.00, 'A', 4, 0),
(1, 'A-5', 'standard', 'available', 50.00, 'A', 5, 0),
(1, 'B-1', 'standard', 'available', 50.00, 'B', 1, 0),
(1, 'B-2', 'standard', 'available', 50.00, 'B', 2, 0),
(1, 'B-3', 'standard', 'available', 50.00, 'B', 3, 0),
(1, 'B-4', 'standard', 'available', 50.00, 'B', 4, 0),
(1, 'B-5', 'standard', 'available', 50.00, 'B', 5, 0),
(1, 'C-1', 'premium', 'available', 60.00, 'C', 1, 0),
(1, 'C-2', 'premium', 'available', 60.00, 'C', 2, 0),
(1, 'C-3', 'premium', 'available', 60.00, 'C', 3, 0),
(1, 'C-4', 'premium', 'available', 60.00, 'C', 4, 0),
(1, 'C-5', 'premium', 'available', 60.00, 'C', 5, 0),
(1, 'D-1', 'ev_charging', 'available', 70.00, 'D', 1, 0),
(1, 'D-2', 'ev_charging', 'available', 70.00, 'D', 2, 0),
(1, 'D-3', 'ev_charging', 'available', 70.00, 'D', 3, 0),
(1, 'D-4', 'ev_charging', 'available', 70.00, 'D', 4, 0),
(1, 'D-5', 'ev_charging', 'available', 70.00, 'D', 5, 0);
