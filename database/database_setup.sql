--Transaction table which store the transactions with unique transaction IDS
CREATE TABLE transactions(
    transaction_id VARCHAR(50) PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT,
    category_id INT NOT NULL, --This is the type of transaction eg payment types
    amount DECIMAL(15, 2) DEFAULT 0.00,
    fee_charged DECIMAL(15, 2) DEFAULT 0.00, --fee charged for the transaction
    transaction_time DATETIME NOT NULL,
    raw_sms_body TEXT, --This is going to be the original text message body


-- --constrains
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
--     --Check whether the amount sent is greater than 0
    CONSTRAINT chk_positive_amount CHECK (amount > 0) 
);
-- --Logging table for all the transactions or storing the transaction histories for all the users
CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50),
    service_center VARCHAR(50),
    protocol_type INT,
    status_code INT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);
