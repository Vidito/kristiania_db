# NordicX Database Application

This is a Streamlit application that demonstrates a database design for a fictional company called NordicX. It implements a fully functional SQLite database with a normalized schema (3NF) and provides a user interface to run various analytical reports.

## Features

- Database Overview: View the raw data in all tables.
- Reports & Analysis: Run pre-defined queries such as Sales by Category, Low Stock Products, and Customer Segmentation.
- Database Design: Documentation on the schema, normalization strategy, and ER diagram.

## Installation

1. Clone the repository.
2. Install the dependencies:
   pip install -r requirements.txt

## Running the App

Run the following command in the project directory:
streamlit run app.py

The application will automatically initialize the database and insert sample data on standard startup.
