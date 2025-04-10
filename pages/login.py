# login.py - User Login
import streamlit as st
import pandas as pd
import os


def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    else:
        return pd.DataFrame(columns=["username", "password"])


def main():
    st.title(" AI-Powered Application for Cancer Support and Personalized Nutrition Recommendation")
    hide_sidebar = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)
    st.title("Login")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")

    if st.button("Login"):
        st.switch_page("pages/chat.py")



if __name__ == "__main__":
    main()
