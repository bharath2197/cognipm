import uuid
import streamlit as st
st.set_page_config(page_title="Cognipm", layout="wide")  # Must be first Streamlit command

from user_auth import add_user, authenticate_user
from cognipm_dashboard import show_dashboard
from dotenv import load_dotenv
load_dotenv()

# --------------------------
# Sign Up UI
# --------------------------
def show_signup():
    st.subheader("Create a New Account")

    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        st.write("DEBUG:", {
            "name": name,
            "email": email,
            "username": username,
            "password": password
        })

        if not all([name, email, username, password]) or \
           not name.strip() or not email.strip() or not username.strip() or not password.strip():
            st.warning("All fields are required.")
        elif add_user(username, name, email, password):
            st.success("🎉 Account created successfully.")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.email = email
            st.rerun()
        else:
            st.error("🚫 Username already exists. Try a different one.")

# --------------------------
# Login UI
# --------------------------
def show_login():
    st.subheader("Login to PM Assistant")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

# --------------------------
# Main App Controller
# --------------------------
def main():
    st.title("AI-Powered Product Management Assistant")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        option = st.radio("Choose an option:", ["Login", "Sign Up"])
        if option == "Login":
            show_login()
        else:
            show_signup()
    else:
        st.sidebar.success(f"Logged in as: {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()
