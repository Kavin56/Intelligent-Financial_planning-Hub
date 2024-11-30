import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Create or connect to an SQLite database with check_same_thread=False
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

# Create or update the table to include a 'date' column (only need to do this once)
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

# Add expense
def app():
    # Check if the user is logged in
    if 'username' not in st.session_state or st.session_state['username'] == '':
        st.warning('Please login first to add expenses.')
        return  # Exit early if not logged in

    st.subheader('Add Expenses')

    # Select between manually adding or uploading a CSV
    option = st.selectbox('Select how to add expenses:', ['Enter Data Manually', 'Upload CSV'])

    if option == 'Enter Data Manually':
        # Add expense form manually
        with st.form(key='expense_form'):
            category = st.selectbox('Select Category', ['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'])
            amount = st.number_input('Amount', min_value=1, step=1)
            description = st.text_input('Description')
            date = st.date_input('Date', value=datetime.today())  # Default to today's date

            submit_button = st.form_submit_button(label='Add Expense')

            if submit_button:
                # Add expense to the SQLite database
                c.execute('INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)',
                          (category, amount, description, date.strftime('%Y-%m-%d')))
                conn.commit()
                st.success(f'Expense added: {category} - ₹ {amount} on {date.strftime("%Y-%m-%d")}')

    elif option == 'Upload CSV':
        # Upload CSV file
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(uploaded_file)

            # Ensure the CSV has the correct columns
            if all(col in df.columns for col in ['category', 'amount', 'description', 'date']):
                # Loop through the rows and insert them into the database
                for _, row in df.iterrows():
                    c.execute('INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)',
                              (row['category'], row['amount'], row['description'], row['date']))
                conn.commit()
                st.success(f'CSV uploaded successfully with {len(df)} entries!')
            else:
                st.error('CSV file must contain the following columns: category, amount, description, date')
