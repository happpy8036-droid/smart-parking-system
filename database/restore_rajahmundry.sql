-- ============================================================
-- Smart Parking System — Safe Rajahmundry Location Repair
-- Database: smart_parking_db
--
-- This script does not delete users, bookings, payments, or slots.
-- It updates the first eight parking-area records used by the demo,
-- hides any extra old locations, and creates fallback slots only
-- when areas 7 or 8 have no slots.
-- ============================================================

USE smart_parking_db;
SET SQL_SAFE_UPDATES = 0;

-- Rajahmundry locations. Do not assume the Uravali row has ID 1:
-- earlier imports may have removed ID 1 and left Uravali under another ID.
UPDATE parking_areas SET
    address = 'Uravali, Inaspet, Rajahmundry',
    city = 'Rajahmundry',
    area = 'Uravali',
    latitude = 17.0005,
    longitude = 81.7825,
    price_per_hour = 50.00,
    open_time = '06:00',
    close_time = '23:00',
    total_slots = 80,
    available_slots = 80,
    description = 'Parking at Uravali Theater area - convenient for moviegoers and shoppers',
    is_active = 1
WHERE name = 'Uravali Theater Parking' AND city = 'Rajahmundry'
LIMIT 1;

INSERT INTO parking_areas
    (name, address, city, area, latitude, longitude, price_per_hour,
     open_time, close_time, total_slots, available_slots, description, is_active)
SELECT 'Uravali Theater Parking', 'Uravali, Inaspet, Rajahmundry',
       'Rajahmundry', 'Uravali', 17.0005, 81.7825, 50.00,
       '06:00', '23:00', 80, 80,
       'Parking at Uravali Theater area - convenient for moviegoers and shoppers', 1
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM parking_areas
    WHERE name = 'Uravali Theater Parking'
      AND city = 'Rajahmundry'
      AND is_active = 1
);

UPDATE parking_areas SET
    name = 'Inorbit Mall Parking',
    address = 'Dantuluru, Rajahmundry',
    city = 'Rajahmundry',
    area = 'Dantuluru',
    latitude = 17.0150,
    longitude = 81.7900,
    price_per_hour = 60.00,
    open_time = '10:00',
    close_time = '22:00',
    total_slots = 150,
    available_slots = 150,
    description = 'Multi-level parking at Inorbit Mall - shopping and dining destination',
    is_active = 1
WHERE id = 2;

UPDATE parking_areas SET
    name = 'Raja Cine Hall Parking',
    address = 'Danavaipet, Rajahmundry',
    city = 'Rajahmundry',
    area = 'Danavaipet',
    latitude = 17.0115,
    longitude = 81.7850,
    price_per_hour = 40.00,
    open_time = '09:00',
    close_time = '23:30',
    total_slots = 60,
    available_slots = 60,
    description = 'Parking near Raja Cine Hall - popular cinema and entertainment hub',
    is_active = 1
WHERE id = 3;

UPDATE parking_areas SET
    name = 'Rajahmundry Bus Stand Parking',
    address = 'Near New Bus Stand, Kovvuru Road',
    city = 'Rajahmundry',
    area = 'Kovvuru Road',
    latitude = 17.0050,
    longitude = 81.7900,
    price_per_hour = 30.00,
    open_time = '00:00',
    close_time = '23:59',
    total_slots = 100,
    available_slots = 100,
    description = 'Public parking near New Bus Stand - for commuters and travelers',
    is_active = 1
WHERE id = 4;

UPDATE parking_areas SET
    name = 'Godavari Bridge Parking',
    address = 'Near Havelock Bridge, Godavari',
    city = 'Rajahmundry',
    area = 'Godavari Bank',
    latitude = 17.0200,
    longitude = 81.7750,
    price_per_hour = 45.00,
    open_time = '06:00',
    close_time = '22:00',
    total_slots = 50,
    available_slots = 50,
    description = 'Scenic parking near the iconic Godavari Bridge - tourist spot',
    is_active = 1
WHERE id = 5;

UPDATE parking_areas SET
    name = 'Apollo Hospital Parking',
    address = 'Rajendra Nagar, Rajahmundry',
    city = 'Rajahmundry',
    area = 'Rajendra Nagar',
    latitude = 17.0080,
    longitude = 81.7880,
    price_per_hour = 55.00,
    open_time = '00:00',
    close_time = '23:59',
    total_slots = 120,
    available_slots = 120,
    description = 'Dedicated parking at Apollo Hospital campus - 24/7 available',
    is_active = 1
WHERE id = 6;

-- Update rows 7 and 8 when they already exist.
UPDATE parking_areas SET
    name = 'Rajamahendravaram Railway Station Parking',
    address = 'Near Railway Station',
    city = 'Rajahmundry',
    area = 'Station Road',
    latitude = 17.0020,
    longitude = 81.7830,
    price_per_hour = 35.00,
    open_time = '00:00',
    close_time = '23:59',
    total_slots = 90,
    available_slots = 90,
    description = 'Long-term and short-term parking near railway station',
    is_active = 1
WHERE id = 7;

UPDATE parking_areas SET
    name = 'Gandhi Chowk Parking',
    address = 'Gandhi Chowk, Rajahmundry',
    city = 'Rajahmundry',
    area = 'Gandhi Chowk',
    latitude = 17.0060,
    longitude = 81.7860,
    price_per_hour = 40.00,
    open_time = '06:00',
    close_time = '23:00',
    total_slots = 70,
    available_slots = 70,
    description = 'Central city parking near Gandhi Chowk - shopping and street food area',
    is_active = 1
WHERE id = 8;

-- If IDs 7 or 8 do not exist, add them without touching existing rows.
INSERT INTO parking_areas
    (id, name, address, city, area, latitude, longitude, price_per_hour,
     open_time, close_time, total_slots, available_slots, description, is_active)
SELECT 7, 'Rajamahendravaram Railway Station Parking', 'Near Railway Station',
       'Rajahmundry', 'Station Road', 17.0020, 81.7830, 35.00,
       '00:00', '23:59', 90, 90,
       'Long-term and short-term parking near railway station', 1
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM parking_areas WHERE id = 7);

INSERT INTO parking_areas
    (id, name, address, city, area, latitude, longitude, price_per_hour,
     open_time, close_time, total_slots, available_slots, description, is_active)
SELECT 8, 'Gandhi Chowk Parking', 'Gandhi Chowk, Rajahmundry',
       'Rajahmundry', 'Gandhi Chowk', 17.0060, 81.7860, 40.00,
       '06:00', '23:00', 70, 70,
       'Central city parking near Gandhi Chowk - shopping and street food area', 1
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM parking_areas WHERE id = 8);

-- Add ten bookable fallback slots only if an area has none.
-- These use area names rather than assumed IDs, so the repaired Uravali
-- row works even if it was recreated with a new auto-increment ID.
INSERT INTO parking_slots
    (area_id, slot_number, slot_type, status, price_per_hour, `row`, `col`, floor)
SELECT a.id, v.slot_number, v.slot_type, 'available', v.price_per_hour,
       v.slot_row, v.slot_col, 1
FROM parking_areas a
JOIN (
    SELECT 'Uravali Theater Parking' AS area_name, 'A-1' AS slot_number, 'standard' AS slot_type, 50.00 AS price_per_hour, 'A' AS slot_row, 1 AS slot_col
    UNION ALL SELECT 'Uravali Theater Parking', 'A-2', 'standard', 50.00, 'A', 2
    UNION ALL SELECT 'Uravali Theater Parking', 'A-3', 'standard', 50.00, 'A', 3
    UNION ALL SELECT 'Uravali Theater Parking', 'A-4', 'standard', 50.00, 'A', 4
    UNION ALL SELECT 'Uravali Theater Parking', 'A-5', 'standard', 50.00, 'A', 5
    UNION ALL SELECT 'Rajamahendravaram Railway Station Parking', 'A-1', 'standard', 35.00, 'A', 1
    UNION ALL SELECT 'Rajamahendravaram Railway Station Parking', 'A-2', 'standard', 35.00, 'A', 2
    UNION ALL SELECT 'Rajamahendravaram Railway Station Parking', 'A-3', 'standard', 35.00, 'A', 3
    UNION ALL SELECT 'Rajamahendravaram Railway Station Parking', 'A-4', 'standard', 35.00, 'A', 4
    UNION ALL SELECT 'Rajamahendravaram Railway Station Parking', 'A-5', 'standard', 35.00, 'A', 5
    UNION ALL SELECT 'Gandhi Chowk Parking', 'A-1', 'standard', 40.00, 'A', 1
    UNION ALL SELECT 'Gandhi Chowk Parking', 'A-2', 'standard', 40.00, 'A', 2
    UNION ALL SELECT 'Gandhi Chowk Parking', 'A-3', 'standard', 40.00, 'A', 3
    UNION ALL SELECT 'Gandhi Chowk Parking', 'A-4', 'standard', 40.00, 'A', 4
    UNION ALL SELECT 'Gandhi Chowk Parking', 'A-5', 'standard', 40.00, 'A', 5
) AS v ON v.area_name = a.name
WHERE a.city = 'Rajahmundry'
  AND NOT EXISTS (
      SELECT 1 FROM parking_slots existing
      WHERE existing.area_id = a.id
  );

-- Hide old Mumbai/demo and unrelated rows. Keep only the eight named
-- Rajahmundry locations active, regardless of their numeric IDs.
UPDATE parking_areas
SET is_active = 0
WHERE NOT (
    city = 'Rajahmundry'
    AND name IN (
        'Uravali Theater Parking',
        'Inorbit Mall Parking',
        'Raja Cine Hall Parking',
        'Rajahmundry Bus Stand Parking',
        'Godavari Bridge Parking',
        'Apollo Hospital Parking',
        'Rajamahendravaram Railway Station Parking',
        'Gandhi Chowk Parking'
    )
);

-- Make the dashboard counts match the slots actually present.
UPDATE parking_areas a
LEFT JOIN (
    SELECT area_id,
           COUNT(*) AS actual_total,
           SUM(status = 'available') AS actual_available
    FROM parking_slots
    GROUP BY area_id
) s ON s.area_id = a.id
SET a.total_slots = COALESCE(s.actual_total, a.total_slots),
    a.available_slots = COALESCE(s.actual_available, 0)
WHERE a.is_active = 1 AND a.city = 'Rajahmundry';

SELECT id, name, city, total_slots, available_slots, is_active
FROM parking_areas
WHERE is_active = 1
ORDER BY id;

-- Expected result: 8 Rajahmundry locations, no Mumbai rows.
