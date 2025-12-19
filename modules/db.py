import sqlite3
import pandas as pd
import streamlit as st

DB_FILE = "nordicx.db" # Using file based DB to persist data across connections

def get_connection():
    return sqlite3.connect(DB_FILE)

def run_query(query, params=None):
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def init_db():
    """Initializes the database with schema and sample data."""
    conn = get_connection()
    c = conn.cursor()
    
    # Enable foreign key support
    c.execute("PRAGMA foreign_keys = ON;")

    # Schema Creation
    schema_sql = """
    -- Drop tables to ensure fresh start (resets AUTOINCREMENT)
    DROP TABLE IF EXISTS Schedule;
    DROP TABLE IF EXISTS Employee;
    DROP TABLE IF EXISTS OrderItem;
    DROP TABLE IF EXISTS `Order`;
    DROP TABLE IF EXISTS Product;
    DROP TABLE IF EXISTS Supplier;
    DROP TABLE IF EXISTS Customer;

    -- Tables
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100) NOT NULL,
        Email VARCHAR(50) UNIQUE NOT NULL,
        Phone VARCHAR(30),
        Address TEXT
    );

    CREATE TABLE IF NOT EXISTS Supplier (
        SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100) NOT NULL,
        ContactInfo VARCHAR(150),
        Address TEXT
    );

    CREATE TABLE IF NOT EXISTS Product (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        SupplierID INT NOT NULL,
        Name VARCHAR(100) NOT NULL,
        Description TEXT,
        Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
        StockLevel INT NOT NULL DEFAULT 0 CHECK (StockLevel >= 0),
        Category VARCHAR(50),
        FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
            ON DELETE RESTRICT ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS `Order` (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INT NOT NULL,
        OrderDate DATE NOT NULL,
        TotalAmount DECIMAL(10, 2) NOT NULL CHECK (TotalAmount >= 0),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            ON DELETE RESTRICT ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS OrderItem (
        OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INT NOT NULL,
        ProductID INT NOT NULL,
        Quantity INT NOT NULL CHECK (Quantity > 0),
        Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
        FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            ON DELETE RESTRICT ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Employee (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100) NOT NULL,
        Position VARCHAR(50),
        Email VARCHAR(50) UNIQUE NOT NULL,
        Phone VARCHAR(30)
    );

    CREATE TABLE IF NOT EXISTS Schedule (
        ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INT NOT NULL,
        ScheduleDate DATE NOT NULL,
        ShiftDetails VARCHAR(100),
        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
            ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
    
    # Data Insertion
    data_sql = """
    -- Customers
    INSERT INTO Customer (Name, Email, Phone, Address) VALUES
    ('Vahid Niamadpour', 'vahid.niamadpour@gmail.com', '+47 123456789', 'Oslo, Norway'),
    ('Gebremariam Assres', 'gebremariam.assres@yahoo.com', '+47 2134658', 'Oslo, Norway'),
    ('John Smith', 'john.smith@hotmail.com', '+46 731234567', 'Gothenburg, Sweden'),
    ('Ole Olesen', 'ole.olesen@mail.dk', '+47 531208755', 'Moss, Norway'),
    ('Ingrid Olsen', 'ingrid.olsen@outlook.com', '+47 98877665', 'Oslo, Norway'),
    ('Erik Svensson', 'erik.svensson@gmail.com', '+46 722334455', 'Malmö, Sweden'),
    ('Kari Nilsen', 'kari.nilsen@online.no', '+47 94455667', 'Bergen, Norway'),
    ('Anna Karlsson', 'anna.karlsson@icloud.com', '+46 733221100', 'Uppsala, Sweden'),
    ('Jonas Berg', 'jonas.berg@mail.se', '+46 744556677', 'Västerås, Sweden'),
    ('Freja Mortensen', 'freja.mortensen@mail.dk', '+45 82233445', 'Odense, Denmark');

    -- Suppliers
    INSERT INTO Supplier (Name, ContactInfo, Address) VALUES
    ('Kristiania AB', 'contact@kristiania.no', 'Oslo, Norway'),
    ('EcoTextiles Nordic', 'sales@ecotextiles.no', 'Trondheim, Norway'),
    ('GreenLiving Supplies', 'info@greenliving.dk', 'Aalborg, Denmark'),
    ('PureCeramics Oy', 'support@pureceramics.fi', 'Helsinki, Finland'),
    ('ScandiHome Essentials', 'orders@scandihome.se', 'Lund, Sweden'),
    ('NordicCraft Supplies', 'hello@nordiccraft.no', 'Bergen, Norway'),
    ('FjordHome Products', 'support@fjordhome.no', 'Stavanger, Norway'),
    ('Arctic Essentials AS', 'contact@arcticessentials.no', 'Tromsø, Norway'),
    ('OsloDesign Partners', 'info@oslopartners.no', 'Oslo, Norway'),
    ('VikingEco Materials', 'sales@vikingeco.no', 'Kristiansand, Norway');

    -- Products
    INSERT INTO Product (SupplierID, Name, Description, Price, StockLevel, Category) VALUES
    (1, 'Oak Wooden Chair', 'Sustainably sourced oak chair', 149.99, 25, 'Furniture'),
    (2, 'Organic Cotton Blanket', 'Soft organic cotton throw blanket', 89.99, 40, 'Textiles'),
    (3, 'Reusable Glass Jars', 'Set of 3 reusable storage jars', 39.99, 50, 'Kitchen'),
    (4, 'Ceramic Dinner Plate', 'Handcrafted ceramic dinner plate', 24.99, 80, 'Tableware'),
    (5, 'Natural Scented Candle', 'Soy wax candle with pine scent', 34.99, 70, 'Lifestyle'),
    (6, 'Handmade Birch Shelf', 'Minimalist birch wall shelf', 129.99, 20, 'Furniture'),
    (7, 'Fjord Wool Rug', 'Thick wool rug inspired by Norwegian fjords', 199.99, 15, 'Textiles'),
    (8, 'Arctic Steel Thermos', 'Insulated thermos for cold climates', 49.99, 60, 'Outdoors'),
    (9, 'Oslo Desk Organizer', 'Modern wooden desk organizer', 59.99, 30, 'Office'),
    (10, 'VikingEco Storage Crate', 'Recycled wood storage crate', 44.99, 40, 'Storage');

    -- Orders
    INSERT INTO `Order` (CustomerID, OrderDate, TotalAmount) VALUES
    (1, '2025-01-10', 189.98),
    (2, '2025-01-12', 299.99),
    (3, '2025-01-15', 59.98),
    (4, '2025-01-18', 149.99),
    (5, '2025-01-20', 89.99),
    (6, '2025-01-22', 74.98),
    (7, '2025-01-25', 39.99),
    (8, '2025-01-27', 119.98),
    (9, '2025-01-28', 34.99),
    (10, '2025-01-30', 44.99);

    -- Order Items
    INSERT INTO OrderItem (OrderID, ProductID, Quantity, Price) VALUES
    (1, 3, 2, 89.99), (2, 2, 1, 299.99), (3, 4, 2, 29.99),
    (4, 1, 1, 149.99), (5, 3, 1, 89.99), (6, 8, 2, 19.99),
    (7, 5, 1, 39.99), (8, 7, 2, 24.99), (9, 9, 1, 34.99),
    (10, 10, 1, 44.99), (1, 6, 1, 19.99), (2, 7, 1, 24.99),
    (3, 5, 1, 39.99), (4, 8, 1, 19.99), (5, 9, 1, 34.99);

    -- Employees
    INSERT INTO Employee (Name, Position, Email, Phone) VALUES
    ('Nils Eriksen', 'Store Manager', 'nils.eriksen@nordicx.com', '+47 701111111'),
    ('Maria Holm', 'Sales Associate', 'maria.holm@nordicx.com', '+47 702222222'),
    ('Oskar Nilsson', 'Inventory Coordinator', 'oskar.nilsson@nordicx.com', '+46 703333333'),
    ('Liv Sørensen', 'Customer Support', 'liv.sorensen@nordicx.com', '+45 81112222'),
    ('Anders Bjorn', 'Warehouse Staff', 'anders.bjorn@nordicx.com', '+47 95554433'),
    ('Elin Karlstad', 'Sales Associate', 'elin.karlstad@nordicx.com', '+46 704444444'),
    ('Thomas Lund', 'Logistics Manager', 'thomas.lund@nordicx.com', '+45 83334444'),
    ('Sara Nyberg', 'Marketing Assistant', 'sara.nyberg@nordicx.com', '+46 705555555'),
    ('Henrik Olsen', 'Store Assistant', 'henrik.olsen@nordicx.com', '+47 92223344'),
    ('Ida Pettersson', 'HR Coordinator', 'ida.pettersson@nordicx.com', '+46 706666666');

    -- Schedules
    INSERT INTO Schedule (EmployeeID, ScheduleDate, ShiftDetails) VALUES
    (1, '2025-02-01', 'Morning Shift'), (2, '2025-02-01', 'Afternoon Shift'),
    (3, '2025-02-01', 'Full Day'), (4, '2025-02-02', 'Morning Shift'),
    (5, '2025-02-02', 'Afternoon Shift'), (6, '2025-02-03', 'Morning Shift'),
    (7, '2025-02-03', 'Full Day'), (8, '2025-02-04', 'Afternoon Shift'),
    (9, '2025-02-04', 'Morning Shift'), (10, '2025-02-05', 'Full Day');

    -- View for Customer Purchase History (Query 9 from scenario)
    CREATE VIEW IF NOT EXISTS CustomerPurchaseHistory AS
    SELECT c.CustomerID, c.Name AS CustomerName, o.OrderID, o.OrderDate,
           o.TotalAmount
    FROM Customer c
    JOIN `Order` o ON c.CustomerID = o.CustomerID;
    """

    try:
        c.executescript(schema_sql)
        c.executescript(data_sql)
        conn.commit()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
