import streamlit as st
from modules import db

def app():
    st.title("🗂️ Database Overview")
    st.subheader("By Vahid Niamadpour for the DB Course.")
    st.text("Explore the raw data in the NordicX database tables.")

    # Get list of tables
    tables = db.run_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    table_names = tables['name'].tolist()

    selected_table = st.selectbox("Select Table", table_names)

    if selected_table:
        df = db.run_query(f"SELECT * FROM `{selected_table}`")
        st.write(f"### Table: {selected_table}")
        st.dataframe(df, use_container_width=True)
        st.caption(f"{len(df)} rows")
