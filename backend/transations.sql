CREATE TABLE transactions (
    sender_acc VARCHAR(10) NOT NULL,
    receiver_acc VARCHAR(10) NOT NULL,
    amount DECIMAL(10,2) DEFAULT 1000 NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_acc) REFERENCES account(acc_no) ON DELETE CASCADE,
    FOREIGN KEY (receiver_acc) REFERENCES account(acc_no) ON DELETE CASCADE
);
