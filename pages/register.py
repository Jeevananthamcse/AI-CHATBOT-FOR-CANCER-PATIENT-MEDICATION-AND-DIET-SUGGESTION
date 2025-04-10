import streamlit as st
import pandas as pd
import os

# Define file path for users.csv
USER_FILE = "users.csv"

# Create users.csv with headers if it does not exist or is empty
if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
    df = pd.DataFrame(columns=["Username", "Password"])
    df.to_csv(USER_FILE, index=False)


# Registration function
def register():
    hide_sidebar = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """
    st.title("AI-Powered Application for Cancer Support and Personalized Nutrition Recommendation")
    st.markdown(hide_sidebar, unsafe_allow_html=True)
    st.title("📝 Register")

    username = st.text_input("Enter a new username")
    password = st.text_input("Enter a password", type="password")

    if st.button("Register"):
        if username and password:
            # Load users and check if file is empty
            users = pd.read_csv(USER_FILE)

            # Ensure correct headers exist
            if "Username" not in users.columns or "Password" not in users.columns:
                st.error("🚨 Error: `users.csv` has incorrect headers! Resetting file...")
                users = pd.DataFrame(columns=["Username", "Password"])
                users.to_csv(USER_FILE, index=False)

            # Check if username already exists
            if username in users["Username"].values:
                st.error("🚨 Username already taken! Try another.")
            else:
                # Append new user
                new_user = pd.DataFrame([[username, password]], columns=["Username", "Password"])
                new_user.to_csv(USER_FILE, mode="a", header=False, index=False)
                st.success("✅ Registration Successful! Please log in.")
                st.switch_page("pages/login.py")  # Redirect to login page
        else:
            st.warning("⚠️ Please fill in all fields.")


register()
