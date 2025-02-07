from flask import Flask, request, jsonify
import mysql.connector
import random
import string
from flask_cors import CORS, cross_origin
import traceback 
app = Flask(__name__)
CORS(app)  # Allow all origins for all routes

# Database Connection
def get_db_connection():
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sharm#@1234',
            database='bms'
        )
        return con
    except mysql.connector.Error as e:
        raise Exception("Database connection failed: " + str(e))

# Generate Unique Account Number
def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

@app.route('/open_account', methods=['POST'])
@cross_origin()
def open_account():
    try:
        data = request.json
        name = data.get('name', '').strip()
        dob = data.get('dob', '').strip()
        address = data.get('address', '').strip()
        balance = float(data.get('balance', 1000))  # Default balance if not provided

        if not all([name, dob, address]):
            return jsonify({'error': 'Missing required fields'}), 400

        con = get_db_connection()
        cur = con.cursor()

        # Ensure unique account number
        acc_no = generate_account_number()
        cur.execute("SELECT acc_no FROM account WHERE acc_no = %s", (acc_no,))
        while cur.fetchone():
            acc_no = generate_account_number()  # Generate again if exists

        cur.execute("INSERT INTO account (name, acc_no, dob, address, balance) VALUES (%s, %s, %s, %s, %s)",
                    (name, acc_no, dob, address, balance))
        con.commit()

        cur.close()
        con.close()

        return jsonify({'message': 'Account successfully created!', 'acc_no': acc_no}), 201

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/transfer', methods=['POST'])
def transfer():
    try:
        data = request.json
        sender_acc = data.get('sender_acc')
        receiver_acc = data.get('receiver_acc')
        amount = float(data.get('amount'))  # Ensure amount is a float

        con = get_db_connection()
        cursor = con.cursor()

        # Check sender balance
        cursor.execute("SELECT balance FROM account WHERE acc_no=%s", (sender_acc,))
        sender = cursor.fetchone()

        if not sender:
            return jsonify({'error': 'Sender account not found'}), 404

        print(f"🔹 Sender Balance: {sender[0]}")  # Debugging

        if float(sender[0]) < amount:
            return jsonify({'error': 'Insufficient balance'}), 400

        # Check receiver exists
        cursor.execute("SELECT balance FROM account WHERE acc_no=%s", (receiver_acc,))
        receiver = cursor.fetchone()

        if not receiver:
            return jsonify({'error': 'Receiver account not found'}), 404

        print(f"🔹 Receiver Balance: {receiver[0]}")  # Debugging

        # Update sender and receiver balances
        new_sender_balance = float(sender[0]) - amount
        new_receiver_balance = float(receiver[0]) + amount

        print(f"✅ New Sender Balance: {new_sender_balance}")
        print(f"✅ New Receiver Balance: {new_receiver_balance}")

        cursor.execute("UPDATE account SET balance=%s WHERE acc_no=%s", (new_sender_balance, sender_acc))
        cursor.execute("UPDATE account SET balance=%s WHERE acc_no=%s", (new_receiver_balance, receiver_acc))

        # Insert transaction record
        cursor.execute(
            "INSERT INTO transactions (sender_acc, receiver_acc, amount, timestamp) VALUES (%s, %s, %s, NOW())",
            (sender_acc, receiver_acc, amount)
        )

        con.commit()
        cursor.close()
        con.close()

        return jsonify({'message': 'Transaction successful!'}), 200

    except Exception as e:
        print("❌ ERROR: ", str(e))
        print(traceback.format_exc())  # Full error stack trace
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


    
@app.route('/balance/<acc_no>', methods=['GET'])
@cross_origin()
def balance(acc_no):
    try:
        con = get_db_connection()
        cur = con.cursor()

        cur.execute("SELECT balance FROM account WHERE acc_no=%s", (acc_no,))
        result = cur.fetchone()

        cur.close()
        con.close()

        if result:
            return jsonify({'balance': result[0]}), 200

        return jsonify({'error': 'Account not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
