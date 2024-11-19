import streamlit as st
from firebase_admin import firestore

def app():
    db = firestore.client()

    try:
        st.title('View Expenses - ' + st.session_state['username'])

        result = db.collection('Expenses').document(st.session_state['username']).get()
        r = result.to_dict()
        expenses = r['expenses']

        def delete_expense(index):
            expense = expenses[index]
            try:
                db.collection('Expenses').document(st.session_state['username']).update({"expenses": firestore.ArrayRemove([expense])})
                st.warning('Expense deleted')
            except:
                st.write('Something went wrong..')

        for index in range(len(expenses)-1, -1, -1):
            st.text_area(label='', value=f"Category: {expenses[index]['category']} \nAmount: {expenses[index]['amount']} USD \nDescription: {expenses[index]['description']}")
            st.button('Delete Expense', on_click=delete_expense, args=(index,), key=index)

    except:
        if st.session_state.username == '':
            st.text('Please Login first')
