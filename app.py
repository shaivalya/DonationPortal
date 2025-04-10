from flask import Flask, render_template, request
import qrcode
import sqlite3
import os
import time  # Added to generate unique filenames

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

YOUR_UPI_ID = "yourupiid"

@app.route('/', methods=['GET', 'POST'])
def donate():
    qr_filename = None
    upi_link = ""

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        amount = request.form.get('amount')

        # Save to DB
        conn = sqlite3.connect('donations.db')
        c = conn.cursor()
        c.execute('INSERT INTO donations (name, email, amount) VALUES (?, ?, ?)', (name, email, amount))
        conn.commit()
        conn.close()

        # Create UPI link
        upi_link = f'upi://pay?pa={YOUR_UPI_ID}&pn=Donation'

        # Generate unique QR filename
        timestamp = int(time.time())
        qr_filename = f'qr_{timestamp}.png'
        qr_path = os.path.join('static', qr_filename)

        # Generate and save QR
        qr_img = qrcode.make(upi_link)
        qr_img.save(qr_path)

        return render_template('donate.html', qr_path=qr_filename, upi_link=upi_link)

    return render_template('donate.html')
if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)





