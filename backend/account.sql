CREATE TABLE account (
    acc_no VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    address TEXT NOT NULL,
    balance DECIMAL(10,2) DEFAULT 1000  -- Default balance set to 1000
);
