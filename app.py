# Import libraries
from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

def total_balance():
    return sum(transaction['amount'] for transaction in transactions)
      
# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance())

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transaction = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))

    # If method is GET (POST has already been dealt with)
    return render_template("form.html")
    
# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        newTransaction = {
            'id': transaction_id,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        for trans in transactions:
            if trans['id'] == transaction_id:
                trans['date'] = newTransaction['date']
                trans['amount'] = newTransaction['amount']
                break
        return redirect(url_for("get_transactions"))
    
    for trans in transactions:
        if trans['id'] == transaction_id:
            return render_template("edit.html", transaction = trans, total_balance=total_balance())

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for trans in transactions:
        if trans['id'] == transaction_id:
            transactions.remove(trans)
            break
    return redirect(url_for("get_transactions"))

# Search for transactions
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        filtered_transactions = []
        for trans in transactions:
            if (trans['amount'] > min and trans['amount'] < max):
                filtered_transactions.append(trans)
        return render_template("transactions.html", transactions = filtered_transactions, total_balance=total_balance())
    
    return render_template("search.html")

# Calculate total of all transactions
@app.route("/balance")
def total_balance():
    total = 0
    for trans in transactions:
        total = total + trans['amount']
    return f"Total Balance: {total}"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)