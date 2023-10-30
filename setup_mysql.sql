CREATE DATABASE IF NOT EXISTS ab_inventory_db;
CREATE USER IF NOT EXISTS 'ab_inventory'@'localhost' IDENTIFIED BY 'ab_123';
GRANT ALL PRIVILEGES ON ab_inventory_db.* TO 'ab_inventory'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ab_inventory'@'localhost';
FLUSH PRIVILEGES;
