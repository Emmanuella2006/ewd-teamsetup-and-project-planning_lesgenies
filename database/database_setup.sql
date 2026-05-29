CREATE DATABASE IF NOT EXISTS momo_data_processor;

USE momo_data_processor;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user_permissions;
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    account_balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE user_permissions(
    user_id INT,
    category_id INT,
    is_allowed BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id) ON DELETE CASCADE
);

CREATE TABLE transactions(
    transaction_id VARCHAR(50) PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT,
    category_id INT NOT NULL,
    amount DECIMAL(15, 2) DEFAULT 0.00,
    fee_charged DECIMAL(15, 2) DEFAULT 0.00,
    transaction_time DATETIME NOT NULL,
    raw_sms_body TEXT,
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
    CONSTRAINT chk_positive_amount CHECK (amount > 0)
);

CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50),
    service_center VARCHAR(50),
    protocol_type INT,
    status_code INT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

INSERT INTO transaction_categories(category_name, description) VALUES
('Money Received', 'Incoming P2P transfers'),
('Payment', 'Outgoing payments for goods/services'),
('Bank Deposit', 'Transfers from MoMo to Bank'),
('Airtime', 'Purchase of mobile airtime/bundles'),
('Transfer', 'Direct P2P transfers to other users');

INSERT INTO users (full_name, phone_number, account_balance) VALUES
('System Centre', '250788110381', 980.00),
('Jane Smith', '250788000013', 0.00),
('Samuel Carter', '250791666666', 0.00),
('Alex Doe', '250791666667', 0.00),
('Linda Green', '250788954321', 0.00);

INSERT INTO user_permissions(user_id, category_id, is_allowed) VALUES (2, 1, TRUE);

INSERT INTO transactions (transaction_id, sender_id, receiver_id, category_id, amount, fee_charged, transaction_time, raw_sms_body) VALUES
('76662021700', 2, 1, 1, 2000.00, 0.00, '2024-05-10 16:30:51', 'You have received 2000 RWF from Jane Smith...'),
('73214484437', 1, 2, 2, 1000.00, 0.00, '2024-05-10 16:31:39', 'TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith...'),
('250795963036', 1, NULL, 3, 40000.00, 0.00, '2024-05-11 18:43:49', 'A bank deposit of 40000 RWF has been added...'),
('1715454249531', 1, 3, 5, 10000.00, 100.00, '2024-05-11 20:34:47', '10000 RWF transferred to Samuel Carter. Fee was: 100 RWF'),
('13913173274', 1, NULL, 4, 2000.00, 0.00, '2024-05-12 11:41:28', 'Your payment of 2000 RWF to Airtime with token...'),
('24227321992', 1, 5, 5, 1600.00, 0.00, '2024-05-14 21:29:01', 'Your payment of 1,600 RWF to Linda Green...'),
('45434420466', 1, 2, 2, 10900.00, 0.00, '2024-05-12 13:26:13', 'Your payment of 10,900 RWF to Jane Smith...');

INSERT INTO system_logs(transaction_id, service_center, protocol_type, status_code) VALUES
('76662021700', '+250788110381', 0, -1),
('73214484437', '+250788110381', 0, -1);
