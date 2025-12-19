import streamlit as st
import plotly.express as px
from modules import db
from datetime import date

def app():
    st.title("📊 Reports & Analysis")

    st.markdown("Select a report to view specific insights from the NordicX database.")
    
    report_type = st.selectbox("Choose Report", [
        "Select a report...",
        "Customers by Purchase Date",
        "Low Stock Products",
        "Employee Work Schedule",
        "Total Sales by Category",
        "Suppliers & Products",
        "Customer Purchase History",
        "High-Value Customers",
        "Top Selling Products",
        "Customer Segmentation"
    ])

    st.divider()

    if report_type == "Customers by Purchase Date":
        st.subheader("Query 4: Customers by Purchase Date Range")
        
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", date(2025, 1, 1))
        end_date = col2.date_input("End Date", date(2025, 1, 31))

        if st.button("Run Query"):
            query = """
            SELECT DISTINCT c.CustomerID, c.Name, c.Email, o.OrderDate
            FROM Customer c
            JOIN `Order` o ON c.CustomerID = o.CustomerID
            WHERE o.OrderDate BETWEEN ? AND ?
            ORDER BY o.OrderDate;
            """
            df = db.run_query(query, (start_date, end_date))
            st.dataframe(df, use_container_width=True)

    elif report_type == "Low Stock Products":
        st.subheader("Query 5: Low Stock Products")
        threshold = st.slider("Stock Threshold", 0, 100, 50)
        
        query = """
        SELECT p.ProductID, p.Name, p.Category, p.StockLevel, p.Price,
               s.Name as SupplierName
        FROM Product p
        INNER JOIN Supplier s ON p.SupplierID = s.SupplierID
        WHERE p.StockLevel < ?
        ORDER BY p.StockLevel ASC;
        """
        df = db.run_query(query, (threshold,))
        
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            fig = px.bar(df, x='Name', y='StockLevel', color='Category', title=f"Products with Stock < {threshold}")
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Employee Work Schedule":
        st.subheader("Query 6: Employee Work Schedule")
        
        # Get employees for dropdown
        employees = db.run_query("SELECT EmployeeID, Name FROM Employee")
        emp_options = {row['Name']: row['EmployeeID'] for _, row in employees.iterrows()}
        selected_emp = st.selectbox("Select Employee", list(emp_options.keys()))
        
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", date(2025, 2, 1))
        end_date = col2.date_input("End Date", date(2025, 2, 5))

        if selected_emp:
            query = """
            SELECT e.EmployeeID, e.Name as EmployeeName, e.Position,
                   s.ScheduleDate, s.ShiftDetails
            FROM Employee e
            INNER JOIN Schedule s ON e.EmployeeID = s.EmployeeID
            WHERE e.EmployeeID = ?
              AND s.ScheduleDate BETWEEN ? AND ?
            ORDER BY s.ScheduleDate;
            """
            df = db.run_query(query, (emp_options[selected_emp], start_date, end_date))
            st.dataframe(df, use_container_width=True)

    elif report_type == "Total Sales by Category":
        st.subheader("Query 7: Total Sales by Product Category")
        
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", date(2025, 1, 1))
        end_date = col2.date_input("End Date", date(2025, 12, 31))

        query = """
        SELECT p.Category, SUM(oi.Quantity * oi.Price) AS TotalSales
        FROM `Order` o
        JOIN OrderItem oi ON o.OrderID = oi.OrderID
        JOIN Product p ON oi.ProductID = p.ProductID
        WHERE o.OrderDate BETWEEN ? AND ?
        GROUP BY p.Category
        ORDER BY TotalSales DESC;
        """
        df = db.run_query(query, (start_date, end_date))
        
        col1, col2 = st.columns([1, 2])
        col1.dataframe(df, use_container_width=True)
        
        if not df.empty:
            fig = px.pie(df, values='TotalSales', names='Category', title="Sales Distribution")
            col2.plotly_chart(fig, use_container_width=True)

    elif report_type == "Suppliers & Products":
        st.subheader("Query 8: Suppliers and Their Products")
        query = """
        SELECT s.SupplierID, s.Name AS SupplierName, s.ContactInfo, s.Address,
               p.Name AS ProductName, p.Category
        FROM Supplier s
        LEFT JOIN Product p ON s.SupplierID = p.SupplierID
        ORDER BY s.Name, p.Name;
        """
        df = db.run_query(query)
        st.dataframe(df, use_container_width=True)

    elif report_type == "Customer Purchase History":
        st.subheader("Query 9: Customer Purchase History View")
        
        # Get customers
        customers = db.run_query("SELECT CustomerID, Name FROM Customer")
        cust_options = {row['Name']: row['CustomerID'] for _, row in customers.iterrows()}
        selected_cust = st.selectbox("Select Customer", list(cust_options.keys()))

        if selected_cust:
            # Note: The View is created in db.py
            query = """
            SELECT * FROM CustomerPurchaseHistory
            WHERE CustomerID = ?
            ORDER BY OrderDate;
            """
            df = db.run_query(query, (cust_options[selected_cust],))
            st.dataframe(df, use_container_width=True)

    elif report_type == "High-Value Customers":
        st.subheader("Query 10.1: High-Value Customers (Above Average Spend)")
        
        query = """
        SELECT c.CustomerID, c.Name, SUM(o.TotalAmount) AS TotalSpent
        FROM Customer c
        JOIN `Order` o ON c.CustomerID = o.CustomerID
        GROUP BY c.CustomerID, c.Name
        HAVING SUM(o.TotalAmount) > (SELECT AVG(TotalAmount) FROM `Order`)
        ORDER BY TotalSpent DESC;
        """
        df = db.run_query(query)
        st.dataframe(df, use_container_width=True)
        
        avg_spend = db.run_query("SELECT AVG(TotalAmount) as Avg FROM `Order`")['Avg'][0]
        st.metric("Average Order Value threshold", f"${avg_spend:.2f}")

    elif report_type == "Top Selling Products":
        st.subheader("Query 10.2: Top 3 Best-Selling Products")
        
        query = """
        SELECT p.ProductID, p.Name, SUM(oi.Quantity) AS TotalUnitsSold
        FROM Product p
        JOIN OrderItem oi ON p.ProductID = oi.ProductID
        GROUP BY p.ProductID, p.Name
        ORDER BY TotalUnitsSold DESC
        LIMIT 3;
        """
        df = db.run_query(query)
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            fig = px.bar(df, x='Name', y='TotalUnitsSold', title="Top 3 Products by Volume")
            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "Customer Segmentation":
        st.subheader("Query 10.3: Customer Segmentation Analysis")
        
        query = """
        SELECT c.CustomerID, c.Name AS CustomerName, c.Email,
               COUNT(o.OrderID) AS TotalOrders,
               COALESCE(SUM(o.TotalAmount), 0) AS AllTimeValue,
               ROUND(COALESCE(AVG(o.TotalAmount), 0), 2) AS AverageOrderValue,
               MIN(o.OrderDate) AS FirstPurchase,
               MAX(o.OrderDate) AS LastPurchase,
               CASE
                   WHEN COUNT(o.OrderID) >= 3 THEN 'VIP Customer'
                   WHEN COUNT(o.OrderID) = 2 THEN 'Regular Customer'
                   WHEN COUNT(o.OrderID) = 1 THEN 'New Customer'
                   ELSE 'No Orders'
               END AS CustomerSegment
        FROM Customer c
        LEFT JOIN `Order` o ON c.CustomerID = o.CustomerID
        GROUP BY c.CustomerID, c.Name, c.Email
        ORDER BY AllTimeValue DESC;
        """
        df = db.run_query(query)
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            segment_counts = df['CustomerSegment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            fig = px.pie(segment_counts, values='Count', names='Segment', title="Customer Segments")
            st.plotly_chart(fig, use_container_width=True)
