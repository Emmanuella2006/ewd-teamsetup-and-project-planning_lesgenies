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
