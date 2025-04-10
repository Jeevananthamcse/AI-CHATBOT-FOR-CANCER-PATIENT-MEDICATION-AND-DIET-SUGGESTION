# index.py - Landing Page
import streamlit as st
import pandas as pd
import os


def main():
    st.set_page_config(page_title="AI-Powered Application for Cancer Support and Personalized Nutrition Recommendation",
                       layout="centered")

    hide_sidebar = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

    st.title("Welcome to AI-Powered Application for Cancer Support and Personalized Nutrition Recommendation")
    st.write("Cancer patients struggle to find reliable diet plans, track symptoms, and monitor progress, often facing emotional stress and uncertainty around treatments. There is a pressing need for a solution that provides timely, accurate, and personalized support. An AI-powered ML-based application can address these challenges by offering tailored diet plans, real-time symptom tracking, and instant responses to cancer-related queries.")

    st.write("### Features:")
    st.markdown("- **Medical Queries**: Get AI-powered responses to your health-related questions.")
    st.markdown("- **Personalized Nutrition**: Receive diet recommendations tailored to your needs.")
    st.markdown("- **Voice Assistance**: Interact using voice commands.")

    st.write("### Get Started:")
    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col1:
        if st.button("Login"):
            st.switch_page("pages/login.py")
    with col2:
        st.write("")  # Small spacing
    with col3:
        if st.button("Register"):
            st.switch_page("pages/register.py")

    # Footer with developer details
    footer = """
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: black;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 16px;
            }
            .footer a {
                color: cyan;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
        <div class="footer">
            Developed by 
            <a href="https://www.linkedin.com/in/prabu" target="_blank">Prabu P</a> | 
            <a href="https://www.linkedin.com/in/arcsith-raj" target="_blank">Arcsith Raj DS</a> | 
            <a href="https://www.linkedin.com/in/jeevanantham" target="_blank">Jeevanantham P</a>
        </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
