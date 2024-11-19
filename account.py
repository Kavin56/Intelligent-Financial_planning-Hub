import streamlit as st
from firebase_admin import auth

def app():
    # Initialize session state variable if not already set
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
        
    if st.session_state['username'] == '':
        st.title("Login / Register to Financial Planning Hub")

        # Choose between login or registration
        option = st.selectbox("Select an option", ["Login", "Register"])
        
        if option == "Login":
            login_form()
        elif option == "Register":
            register_form()

def login_form():
    st.subheader("Login")
    
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            try:
                # Attempt to authenticate the user using Firebase Authentication
                user = auth.get_user_by_email(username)
                if user and user.password == password:
                    st.session_state['username'] = username
                    st.success(f"Welcome, {st.session_state['username']}!")
                else:
                    st.error("Invalid credentials, please try again.")
            except:
                st.error("An error occurred while logging in. Please try again.")

def register_form():
    st.subheader("Register")
    
    with st.form(key='register_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_button = st.form_submit_button("Register")
        
        if register_button:
            if password == confirm_password:
                try:
                    # Attempt to create a new user in Firebase
                    user = auth.create_user(
                        email=username,
                        password=password,
                    )
                    st.session_state['username'] = username
                    st.success(f"Registration successful! Welcome, {st.session_state['username']}!")
                except:
                    st.error("An error occurred during registration. Please try again.")
            else:
                st.error("Passwords do not match. Please try again.")
