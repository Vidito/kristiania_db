import streamlit as st
from modules import db, home, reports, about

# Page Config
st.set_page_config(
    page_title="NordicX Database Manager",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Call db init on startup to ensure in-memory DB is populated
if 'db_initialized' not in st.session_state:
    db.init_db()
    st.session_state['db_initialized'] = True

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("NordicX Manager ❄️")
page = st.sidebar.radio("Navigation", ["Overview", "Reports & Analysis", "Database Design"])

st.sidebar.markdown("---")
st.sidebar.info("Using In-Memory SQLite Database")

# Routing
if page == "Overview":
    home.app()
elif page == "Reports & Analysis":
    reports.app()
elif page == "Database Design":
    about.app()
