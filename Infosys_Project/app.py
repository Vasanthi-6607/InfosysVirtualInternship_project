import streamlit as st
from database import create_table, add_user, login_user

st.set_page_config(page_title="Login App", layout="centered")

create_table()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Login"

st.title("🔐 User Login System")

# ---------------- SIGNUP ----------------
def signup():
    st.subheader("📝 Create New Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Signup")

        if submit:
            try:
                add_user(username, password)
                st.success("Account created successfully! Please login.")
                st.session_state.page = "Login"
                st.experimental_rerun()
            except:
                st.error("Username already exists")

# ---------------- LOGIN ----------------
def login():
    st.subheader("🔑 Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            result = login_user(username, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.page = "Home"
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

# ---------------- HOME ----------------
def home():
    st.subheader("🏠 Home Page")
    st.success(f"Welcome, **{st.session_state.user}** 👋")
    st.write("You are successfully logged in.")

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "Login"
        st.experimental_rerun()

# ---------------- PAGE ROUTING ----------------
if st.session_state.page == "Login":
    login()
    st.write("New user?")
    if st.button("Create an account"):
        st.session_state.page = "Signup"
        st.experimental_rerun()

elif st.session_state.page == "Signup":
    signup()
    if st.button("Back to Login"):
        st.session_state.page = "Login"
        st.experimental_rerun()

elif st.session_state.page == "Home":
    if "logged_in" in st.session_state:
        home()
    else:
        st.session_state.page = "Login"
        st.experimental_rerun()
