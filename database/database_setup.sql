CREATE DATABASE IF NOT EXISTS momo_data_processor;

USE momo_data_processor;

-- Escape to be able to run the file multiple times without having to update the tables
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- --CREATE TABLES
-- --Users table with the cardinality of 1:M with the transactions
CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    account_balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--     COMMENT 'Stores the sender and receiver information.'
);

-- --Table to show the available categories of transactions
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
--     COMMENT 'Types of transactions: Deposit, Withdrawal, Airtime, etc.'
);

CREATE TABLE user_permissions(
    user_id INT,
    category_id INT,
    is_allowed BOOLEAN DEFAULT TRUE,

    PRIMARY KEY (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) ON DELETE CASCADE
);

