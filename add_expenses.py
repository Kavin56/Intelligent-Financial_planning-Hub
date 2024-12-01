import os
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
USER_PHONE_NUMBER = os.getenv('USER_PHONE_NUMBER')

# Ensure Twilio configuration is complete
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, USER_PHONE_NUMBER]):
    raise ValueError("Twilio configuration is incomplete. Check your .env file.")

# Connect to SQLite database
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

# Create the expenses table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        description TEXT,
        date TEXT
    )
''')
conn.commit()

# Send SMS alert using Twilio
def send_sms_alert(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=USER_PHONE_NUMBER
    )

# Check category thresholds
def check_thresholds():
    thresholds = {
        'Food': 3000,
        'Transport': 1500,
        'Entertainment': 1000
    }

    # Fetch expenses grouped by category
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = c.fetchall()

    for category, total in rows:
        if category in thresholds and total > thresholds[category]:
            alert_message = f"Alert! {category} expenses exceeded the limit. Total: ₹{total}, Limit: ₹{thresholds[category]}"
            st.warning(alert_message)
            send_sms_alert(alert_message)

# Streamlit app
def app():
    if 'username' not in st.session_state or st.session_state['username'] == '':
        st.warning('Please login first to add expenses.')
        return

    st.subheader('Add Expenses')

    option = st.selectbox('Select how to add expenses:', ['Enter Data Manually', 'Upload CSV'])

    if option == 'Enter Data Manually':
        with st.form(key='expense_form'):
            category = st.selectbox('Select Category', ['Food', 'Transport', 'Utilities', 'Entertainment', 'Stocks/Mutual Fund', 'Others'])
            amount = st.number_input('Amount', min_value=1, step=1)
            description = st.text_input('Description')
            date = st.date_input('Date', value=datetime.today())

            submit_button = st.form_submit_button(label='Add Expense')

            if submit_button:
                c.execute('INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)',
                          (category, amount, description, date.strftime('%Y-%m-%d')))
                conn.commit()
                st.success(f'Expense added: {category} - ₹{amount} on {date.strftime("%Y-%m-%d")}')
                check_thresholds()

    elif option == 'Upload CSV':
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file:
            df = pd.read_csv(uploaded_file)

            if all(col in df.columns for col in ['category', 'amount', 'description', 'date']):
                for _, row in df.iterrows():
                    c.execute('INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)',
                              (row['category'], row['amount'], row['description'], row['date']))
                conn.commit()
                st.success(f'CSV uploaded successfully with {len(df)} entries!')
                check_thresholds()
            else:
                st.error('CSV file must contain the following columns: category, amount, description, date')

if __name__ == "__main__":
    app()
