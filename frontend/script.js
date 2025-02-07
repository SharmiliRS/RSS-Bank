async function openAccount() {
    const name = document.getElementById("name").value.trim();
    const dob = document.getElementById("dob").value;
    const address = document.getElementById("address").value.trim();
    const balance = document.getElementById("balance").value;

    if (!name || !dob || !address || !balance) {
        alert("⚠️ Please fill in all the fields.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/open_account", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, dob, address, balance })
        });

        const data = await response.json();

        if (response.ok) {
            // Display Account Details in UI
            document.getElementById("result").innerHTML = `
                <div class="success-message">
                    <p>✅ <strong>${data.message}</strong></p>
                    <p><strong>Account Number:</strong> <span id="acc-number">${data.acc_no}</span></p>
                </div>
            `;
            document.getElementById("result").style.display = "block";

            // Alert success message
            alert(`🎉 Account Created Successfully!\nYour Account Number: ${data.acc_no}`);

            // Optional: Clear form fields
            document.getElementById("accountForm").reset();
        } else {
            document.getElementById("result").innerHTML = `<p class="error-message">❌ ${data.error}</p>`;
            document.getElementById("result").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<p class="error-message">❌ Something went wrong. Please try again later.</p>`;
    }
}
async function checkBalance() {
    const acc_no = document.getElementById("acc_no").value.trim();

    if (!acc_no) {
        alert("⚠️ Please enter your Account Number.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/balance/${acc_no}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("balance-result").innerHTML = `
                <div class="success-message">
                    <p>💰 <strong>Current Balance:</strong> ₹${data.balance}</p>
                </div>
            `;
        } else {
            document.getElementById("balance-result").innerHTML = `<p class="error-message">❌ ${data.error}</p>`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("balance-result").innerHTML = `<p class="error-message">❌ Something went wrong. Please try again.</p>`;
    }
}
async function transferFunds() {
    const sender_acc = document.getElementById("sender_acc").value.trim();
    const receiver_acc = document.getElementById("receiver_acc").value.trim();
    const amount = parseFloat(document.getElementById("amount").value.trim());

    console.log("Sender Account:", sender_acc);  // Debugging

    if (!sender_acc || !receiver_acc || isNaN(amount) || amount <= 0) {
        alert("⚠️ Please fill all fields correctly.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/transfer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sender_acc, receiver_acc, amount })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("transfer-result").innerHTML = `
                <div class="success-message">
                    <p>✅ ${data.message}</p>
                </div>
            `;
        } else {
            document.getElementById("transfer-result").innerHTML = `
                <p class="error-message">❌ ${data.error}</p>
            `;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("transfer-result").innerHTML = `
            <p class="error-message">❌ Something went wrong. Please try again.</p>
        `;
    }
}
