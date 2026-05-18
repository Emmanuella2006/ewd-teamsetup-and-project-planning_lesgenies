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
--Inserting into transactions categories

INSERT INTO transaction_categories(category_name, description) VALUES
("Money Received", "Incoming P2P transfers"),
("Payment", "Outgoing payments for goods/services"),
("Bank Deposit", "Transfers from MoMo to Bank"),
("Airtime", "Purchase of mobile airtime/bundles"),
("Transfer", "Direct P2P transfers to other users");

INSERT INTO users (full_name, phone_number, account_balance) VALUES
('System Owner', '250788110381', 980.00),
('Jane Smith', '250788******013', 0.00),
('Samuel Carter', '250791666666', 0.00),
('Alex Doe', '250791666667', 0.00),
('Linda Green', '250788954321', 0.00);

INSERT INTO user_permissions (user_id, category_id, is_allowed)
SELECT 1, category_id, TRUE FROM transaction_categories;

INSERT INTO user_permissions(user_id, category_id, is_allowed) VALUES (2, 1, TRUE);

INSERT INTO transactions (transaction_id, sender_id, receiver_id, category_id, amount, fee_charged, transaction_time, raw_sms_body) VALUES
('76662021700', 2, 1, 1, 2000.00, 0.00, '2024-05-10 16:30:51', 'You have received 2000 RWF from Jane Smith...'),
('73214484437', 1, 2, 2, 1000.00, 0.00, '2024-05-10 16:31:39', 'TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith...'),
('250795963036', NULL, 1, 3, 40000.00, 0.00, '2024-05-11 18:43:49', 'A bank deposit of 40000 RWF has been added...'),
('1715454249531', 1, 3, 5, 10000.00, 100.00, '2024-05-11 20:34:47', '10000 RWF transferred to Samuel Carter. Fee was: 100 RWF'),
('13913173274', 1, NULL, 4, 2000.00, 0.00, '2024-05-12 11:41:28', 'Your payment of 2000 RWF to Airtime with token...'),
('24227321992', 1, 5, 5, 1600.00, 0.00, '2024-05-14 21:29:01', 'Your payment of 1,600 RWF to Linda Green...'),
('45434420466', 1, 2, 2, 10900.00, 0.00, '2024-05-12 13:26:13', 'Your payment of 10,900 RWF to Jane Smith...');

INSERT INTO system_logs(transaction_id, service_center, protocol_type, status_code) VALUES
('76662021700', '+250788110381', 0, -1),
('73214484437', '+250788110381', 0, -1),
('250795963036', '+250788110381', 0, -1);
