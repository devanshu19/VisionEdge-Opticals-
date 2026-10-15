-- ========================================================
-- VisionEdge Complete XAMPP MySQL Database Schema & Seed Data
-- Database Name: visionedge_db
-- Compatibility: XAMPP / phpMyAdmin / MySQL 5.7+ / MySQL 8.0+
-- ========================================================

CREATE DATABASE IF NOT EXISTS `visionedge_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `visionedge_db`;

SET FOREIGN_KEY_CHECKS = 0;

-- --------------------------------------------------------
-- 1. Table structure for table `user`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `first_name` VARCHAR(50) DEFAULT NULL,
  `last_name` VARCHAR(50) DEFAULT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `email` VARCHAR(120) DEFAULT NULL UNIQUE,
  `phone` VARCHAR(20) DEFAULT NULL,
  `gender` VARCHAR(20) DEFAULT NULL,
  `date_of_birth` DATE DEFAULT NULL,
  `address` TEXT DEFAULT NULL,
  `role` VARCHAR(50) DEFAULT 'customer',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 2. Table structure for table `customer`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_code` VARCHAR(20) DEFAULT NULL UNIQUE,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `gender` VARCHAR(20) DEFAULT NULL,
  `date_of_birth` DATE DEFAULT NULL,
  `age` INT DEFAULT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `alternate_phone` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(120) DEFAULT NULL,
  `address` TEXT DEFAULT NULL,
  `city` VARCHAR(100) DEFAULT NULL,
  `state` VARCHAR(100) DEFAULT NULL,
  `pincode` VARCHAR(20) DEFAULT NULL,
  `occupation` VARCHAR(100) DEFAULT NULL,
  `photo` VARCHAR(255) DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT 'Active',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` INT DEFAULT NULL,
  INDEX `idx_customer_phone` (`phone`),
  INDEX `idx_customer_email` (`email`),
  CONSTRAINT `fk_customer_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 3. Table structure for table `customer_profile`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `customer_profile`;
CREATE TABLE `customer_profile` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL UNIQUE,
  `blood_group` VARCHAR(10) DEFAULT NULL,
  `eye_conditions` TEXT DEFAULT NULL,
  `allergies` TEXT DEFAULT NULL,
  `notes` TEXT DEFAULT NULL,
  CONSTRAINT `fk_profile_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 4. Table structure for table `appointment`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `appointment`;
CREATE TABLE `appointment` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL,
  `appointment_date` DATE NOT NULL,
  `appointment_time` TIME NOT NULL,
  `appointment_type` VARCHAR(50) DEFAULT 'Eye Test',
  `doctor_name` VARCHAR(100) DEFAULT NULL,
  `status` VARCHAR(50) DEFAULT 'Pending',
  `notes` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_appointment_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 5. Table structure for table `eye_test`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `eye_test`;
CREATE TABLE `eye_test` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL,
  `appointment_id` INT DEFAULT NULL,
  `right_sphere` VARCHAR(20) DEFAULT NULL,
  `right_cylinder` VARCHAR(20) DEFAULT NULL,
  `right_axis` VARCHAR(20) DEFAULT NULL,
  `left_sphere` VARCHAR(20) DEFAULT NULL,
  `left_cylinder` VARCHAR(20) DEFAULT NULL,
  `left_axis` VARCHAR(20) DEFAULT NULL,
  `pd_value` VARCHAR(20) DEFAULT NULL,
  `remarks` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_eyetest_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_eyetest_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 6. Table structure for table `prescription`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `prescription`;
CREATE TABLE `prescription` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `prescription_number` VARCHAR(50) DEFAULT NULL UNIQUE,
  `customer_id` INT NOT NULL,
  `eye_test_id` INT DEFAULT NULL,
  `add_power` VARCHAR(20) DEFAULT NULL,
  `prescription_image` VARCHAR(255) DEFAULT NULL,
  `ai_extracted_text` TEXT DEFAULT NULL,
  `confidence_score` FLOAT DEFAULT NULL,
  `doctor_name` VARCHAR(100) DEFAULT NULL,
  `date` DATE DEFAULT NULL,
  `expiry_date` DATE DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT 'Completed',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_prescription_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_prescription_eyetest` FOREIGN KEY (`eye_test_id`) REFERENCES `eye_test` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 7. Table structure for table `frame`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `frame`;
CREATE TABLE `frame` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `frame_code` VARCHAR(50) DEFAULT NULL UNIQUE,
  `brand` VARCHAR(100) DEFAULT NULL,
  `model` VARCHAR(100) DEFAULT NULL,
  `name` VARCHAR(150) DEFAULT NULL,
  `shape` VARCHAR(50) DEFAULT NULL,
  `color` VARCHAR(50) DEFAULT NULL,
  `size` VARCHAR(50) DEFAULT NULL,
  `material` VARCHAR(50) DEFAULT NULL,
  `gender` VARCHAR(20) DEFAULT NULL,
  `price` FLOAT NOT NULL DEFAULT 0.0,
  `selling_price` FLOAT DEFAULT NULL,
  `stock` INT DEFAULT 0,
  `min_stock` INT DEFAULT 5,
  `image` VARCHAR(255) DEFAULT NULL,
  `vto_image` VARCHAR(255) DEFAULT NULL,
  `status` VARCHAR(50) DEFAULT 'Available',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 8. Table structure for table `lens`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `lens`;
CREATE TABLE `lens` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `lens_code` VARCHAR(50) DEFAULT NULL UNIQUE,
  `name` VARCHAR(150) DEFAULT NULL,
  `brand` VARCHAR(100) DEFAULT NULL,
  `type` VARCHAR(50) DEFAULT NULL,
  `lens_type` VARCHAR(50) DEFAULT NULL,
  `coating` VARCHAR(100) DEFAULT NULL,
  `price` FLOAT NOT NULL DEFAULT 0.0,
  `selling_price` FLOAT DEFAULT NULL,
  `stock` INT DEFAULT 0,
  `min_stock` INT DEFAULT 10,
  `image` VARCHAR(255) DEFAULT NULL,
  `status` VARCHAR(50) DEFAULT 'Available',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 9. Table structure for table `supplier`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `supplier`;
CREATE TABLE `supplier` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(120) DEFAULT NULL,
  `address` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 10. Table structure for table `order`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` VARCHAR(50) DEFAULT NULL UNIQUE,
  `order_number` VARCHAR(50) DEFAULT NULL UNIQUE,
  `customer_id` INT NOT NULL,
  `prescription_id` INT DEFAULT NULL,
  `status` VARCHAR(50) DEFAULT 'Pending',
  `total_amount` FLOAT DEFAULT 0.0,
  `order_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_order_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_prescription` FOREIGN KEY (`prescription_id`) REFERENCES `prescription` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 11. Table structure for table `order_item`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `order_item`;
CREATE TABLE `order_item` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `product_type` VARCHAR(50) DEFAULT NULL,
  `item_type` VARCHAR(50) DEFAULT NULL,
  `product_id` INT DEFAULT NULL,
  `item_id` INT DEFAULT NULL,
  `quantity` INT DEFAULT 1,
  `price` FLOAT DEFAULT 0.0,
  `total_price` FLOAT DEFAULT 0.0,
  CONSTRAINT `fk_item_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 12. Table structure for table `billing`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `billing`;
CREATE TABLE `billing` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `invoice_number` VARCHAR(50) NOT NULL UNIQUE,
  `order_id` INT NOT NULL,
  `subtotal` FLOAT DEFAULT 0.0,
  `discount` FLOAT DEFAULT 0.0,
  `gst` FLOAT DEFAULT 0.0,
  `total_amount` FLOAT NOT NULL DEFAULT 0.0,
  `payment_status` VARCHAR(20) DEFAULT 'Pending',
  `payment_method` VARCHAR(50) DEFAULT 'Cash',
  `invoice_pdf` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_billing_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 13. Table structure for table `payment`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `payment`;
CREATE TABLE `payment` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `billing_id` INT NOT NULL,
  `amount` FLOAT NOT NULL DEFAULT 0.0,
  `transaction_id` VARCHAR(100) DEFAULT NULL,
  `payment_method` VARCHAR(50) DEFAULT NULL,
  `payment_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_payment_billing` FOREIGN KEY (`billing_id`) REFERENCES `billing` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 14. Table structure for table `frame_recommendation`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `frame_recommendation`;
CREATE TABLE `frame_recommendation` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL,
  `face_shape` VARCHAR(50) DEFAULT NULL,
  `face_image` VARCHAR(255) DEFAULT NULL,
  `recommended_frames` TEXT DEFAULT NULL,
  `selected_frame` VARCHAR(100) DEFAULT NULL,
  `ai_reason` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_framerec_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 15. Table structure for table `lens_recommendation`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `lens_recommendation`;
CREATE TABLE `lens_recommendation` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT DEFAULT NULL,
  `prescription_id` INT DEFAULT NULL,
  `recommended_lens` TEXT DEFAULT NULL,
  `reason` TEXT DEFAULT NULL,
  `ai_response` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_lensrec_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_lensrec_prescription` FOREIGN KEY (`prescription_id`) REFERENCES `prescription` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 16. Table structure for table `virtual_try_on_history`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `virtual_try_on_history`;
CREATE TABLE `virtual_try_on_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL,
  `frame_id` INT NOT NULL,
  `original_image` VARCHAR(255) DEFAULT NULL,
  `generated_image` VARCHAR(255) DEFAULT NULL,
  `tryon_image` VARCHAR(255) DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_vto_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_vto_frame` FOREIGN KEY (`frame_id`) REFERENCES `frame` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 17. Table structure for table `chat_history`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT DEFAULT NULL,
  `customer_id` INT DEFAULT NULL,
  `question` TEXT NOT NULL,
  `answer` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_chathistory_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_chathistory_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 18. Table structure for table `notification`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT DEFAULT NULL,
  `customer_id` INT DEFAULT NULL,
  `notification_type` VARCHAR(50) NOT NULL,
  `title` VARCHAR(150) NOT NULL,
  `message` TEXT NOT NULL,
  `status` VARCHAR(20) DEFAULT 'Unread',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_notif_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_notif_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 19. Table structure for table `inventory_transaction`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `inventory_transaction`;
CREATE TABLE `inventory_transaction` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `product_type` VARCHAR(50) DEFAULT NULL,
  `product_id` INT DEFAULT NULL,
  `transaction_type` VARCHAR(50) DEFAULT NULL,
  `quantity` INT DEFAULT 0,
  `notes` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 20. Table structure for table `brand`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `brand`;
CREATE TABLE `brand` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 21. Table structure for table `category`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 22. Table structure for table `order_status_history`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `order_status_history`;
CREATE TABLE `order_status_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `status` VARCHAR(50) DEFAULT NULL,
  `notes` TEXT DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statushistory_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- 23. Table structure for table `audit_log`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `audit_log`;
CREATE TABLE `audit_log` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT DEFAULT NULL,
  `action` VARCHAR(100) DEFAULT NULL,
  `module` VARCHAR(100) DEFAULT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_audit_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- ========================================================
-- Seed Data Insertion
-- ========================================================

-- Insert Default Admin Account
INSERT INTO `user` (`username`, `first_name`, `last_name`, `password_hash`, `email`, `role`) VALUES
('admin', 'System', 'Administrator', 'scrypt:32768:8:1$7QyXw3x1$5c4b1234567890abcdef', 'admin@visionedge.com', 'admin');

-- Insert Sample Suppliers
INSERT INTO `supplier` (`name`, `phone`, `email`, `address`) VALUES
('Ray-Ban Eyewear Supplier', '9876543210', 'supplier@rayban.com', 'Mumbai, India'),
('Essilor Optical Lenses', '9876543211', 'contact@essilor.com', 'Delhi, India');

-- Insert Sample Frames
INSERT INTO `frame` (`frame_code`, `brand`, `model`, `name`, `shape`, `color`, `size`, `material`, `gender`, `price`, `stock`, `min_stock`, `status`) VALUES
('FRM001', 'Ray-Ban', 'Wayfarer Classic', 'Ray-Ban Wayfarer Classic', 'Square', 'Black', 'Medium', 'Acetate', 'Unisex', 4500.0, 25, 5, 'Available'),
('FRM002', 'Oakley', 'Holbrook Sport', 'Oakley Holbrook Sport', 'Rectangle', 'Matte Black', 'Large', 'O-Matter', 'Men', 5200.0, 18, 5, 'Available'),
('FRM003', 'Vogue', 'Cat-Eye Elegance', 'Vogue Cat-Eye Elegance', 'Cat-Eye', 'Rose Gold', 'Small', 'Metal', 'Women', 3800.0, 12, 3, 'Available');

-- Insert Sample Lenses
INSERT INTO `lens` (`lens_code`, `name`, `brand`, `type`, `coating`, `price`, `stock`, `min_stock`, `status`) VALUES
('LNS001', 'Essilor Crizal Anti-Glare', 'Essilor', 'Single Vision', 'Anti-Glare', 1800.0, 40, 10, 'Available'),
('LNS002', 'Zeiss BlueGuard Photochromic', 'Zeiss', 'Progressive', 'Blue Cut + Anti-Reflective', 3500.0, 30, 8, 'Available');

-- Insert Sample Customer
INSERT INTO `customer` (`customer_code`, `first_name`, `last_name`, `gender`, `age`, `phone`, `email`, `city`, `status`) VALUES
('CUST001', 'Rahul', 'Sharma', 'Male', 29, '9812345678', 'rahul.sharma@example.com', 'Mumbai', 'Active');

INSERT INTO `customer_profile` (`customer_id`, `blood_group`, `eye_conditions`, `allergies`, `notes`) VALUES
(1, 'O+', 'Mild Myopia', 'None', 'Prefers lightweight titanium frames');

-- Insert Sample Appointment
INSERT INTO `appointment` (`customer_id`, `appointment_date`, `appointment_time`, `appointment_type`, `doctor_name`, `status`) VALUES
(1, '2026-08-15', '10:30:00', 'Eye Test', 'Dr. Smith', 'Confirmed');
