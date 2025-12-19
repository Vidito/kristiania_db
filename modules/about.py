import streamlit as st

def app():
    st.title("📐 Database Design & Architecture")
    
    st.markdown("""
    ## 1. Database Schema
    The NordicX database is designed to handle an e-commerce system with the following core entities:
    - **Customer**: Stores customer details.
    - **Supplier**: Manages supplier information.
    - **Product**: Inventory items linked to suppliers.
    - **Order**: Customer orders.
    - **OrderItem**: Line items for each order (Many-to-Many resolution).
    - **Employee**: Staff members.
    - **Schedule**: Employee shifts.
    """)

    col1, col2, col3= st.columns([1,2,1])

    with col2:
        st.image("er.png", caption="Entity-Relationship Diagram", width='content')

    st.markdown("---")

    st.subheader("2. Normalization Strategy")
    st.markdown("""
    The schema is normalized to **3NF (Third Normal Form)**:
    - **1NF**: Atomic values (no multi-value fields).
    - **2NF**: No partial dependencies (e.g., product details depend fully on ProductID).
    - **3NF**: No transitive dependencies (e.g., supplier info is referenced via Foreign Key).
    
    **Key Benefits:**
    - tailored ON DELETE/UPDATE actions (RESTRICT/CASCADE).
    - Efficient querying.
    - Reduced data redundancy.
    """)

    st.markdown("---")

    st.subheader("3. ACID Properties")
    st.success("**Atomicity**")
    st.markdown("Transactions are 'all or nothing'. If an order fails mid-process (e.g., stock update fails), the entire transaction rolls back.")
    
    st.info("**Consistency**")
    st.markdown("Data adheres to predefined constraints (e.g., Price >= 0, StockLevel >= 0). This ensures the database always remains in a valid state.")

    st.markdown("---")

    st.subheader("4. Why Relational vs. NoSQL?")
    st.markdown("""
    **Chosen: Relational (SQL)**
    - Strong relationships between entities (Foreign Keys).
    - Structured data with fixed schemas.
    - Complex queries/joins are required (e.g., Sales by Category).
    
    **Why not NoSQL?**
    - Data is highly structured, not unstructured.
    - ACID compliance is critical for financial transactions (Orders).
    - Join operations would be inefficient in NoSQL.
    """)
    
    st.markdown("---")
    st.caption("NordicX Database Documentation")
