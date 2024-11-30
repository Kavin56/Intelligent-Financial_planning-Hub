import streamlit as st
import sqlite3
import pandas as pd

# Create or connect to an SQLite database
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

def app():
    # Check if the user is logged in by checking 'username' in session state
    if 'username' not in st.session_state or st.session_state['username'] == '':
        st.warning('Please login first to view your expenses.')
        return  # Exit early if not logged in

    st.title('View Expenses - ' + st.session_state['username'])

    try:
        # Fetch all expenses from the database
        c.execute('SELECT id, category, amount, description, date FROM expenses')
        expenses = c.fetchall()

        if len(expenses) > 0:
            # Display expenses in a table
            df = pd.DataFrame(expenses, columns=['ID', 'Category', 'Amount', 'Description', 'Date'])

            # Display the dataframe in the Streamlit app
            st.dataframe(df)

            # Allow user to select an entry to delete
            expense_to_delete = st.selectbox('Select an expense to delete:', df['ID'])

            if st.button('Delete Selected Expense'):
                # Delete the selected expense by ID
                c.execute('DELETE FROM expenses WHERE id = ?', (expense_to_delete,))
                conn.commit()
                st.success(f'Expense with ID {expense_to_delete} has been deleted.')

                # Refresh the displayed table after deletion
                c.execute('SELECT id, category, amount, description, date FROM expenses')
                expenses = c.fetchall()
                df = pd.DataFrame(expenses, columns=['ID', 'Category', 'Amount', 'Description', 'Date'])
                st.dataframe(df)
        else:
            st.warning('No expenses found.')

    except Exception as e:
        st.error(f"An error occurred: {e}")
