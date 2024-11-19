import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
load_dotenv()

# Import the app modules
import home, add_expenses, account, view_expenses, about, dashboard

st.set_page_config(
    page_title="Financial Planning Hub",
)

# Google Analytics
st.markdown(
    """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src=f"https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', os.getenv('analytics_tag'));
        </script>
    """, unsafe_allow_html=True)

# Define the MultiApp class
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Add an app to the list."""
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        """Run the selected app."""
        # Sidebar with app options
        with st.sidebar:
            app = option_menu(
                menu_title='Financial Planning Hub',
                options=['Home', 'Account', 'Add Expenses', 'View Expenses', 'Dashboard', 'About'],
                icons=['house-fill', 'person-circle', 'plus-circle', 'list', 'graph-up', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Execute the selected app
        if app == "Home":
            home.app()
        elif app == "Account":
            account.app()
        elif app == "Add Expenses":
            add_expenses.app()
        elif app == "View Expenses":
            view_expenses.app()
        elif app == "Dashboard":
            dashboard.app()
        elif app == "About":
            about.app()


# Create an instance of the MultiApp class and run it
if __name__ == "__main__":
    multi_app = MultiApp()  # Create the instance
    multi_app.run()  # Run the app
