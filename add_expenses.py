import streamlit as st

def app():
    st.subheader('Add Expenses')

    # Add expense form
    with st.form(key='expense_form'):
        category = st.selectbox('Select Category', ['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'])
        amount = st.number_input('Amount', min_value=0.01, step=0.01)
        description = st.text_input('Description')

        submit_button = st.form_submit_button(label='Add Expense')

        if submit_button:
            # Add code here to save expense data (e.g., Firebase or database)
            st.success(f'Expense added: {category} - ₹ {amount} ')
