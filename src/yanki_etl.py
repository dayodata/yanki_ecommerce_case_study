# Importing necessary libraries
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


## Extraction layer
#yanki_df = pd.read_csv(r"C:\Users\olada\OneDrive\Documents\Data Engineering Folder\Python\Yanki_ecommerce_case_study\dataset\raw_data\yanki_ecommerce.csv")
yanki_df = pd.read_csv(r"dataset\raw_data\yanki_ecommerce.csv")

pd.set_option('display.max_columns', None)

print(yanki_df.head())

print('----------------------------------------------------------------')
print(yanki_df.describe())

print('---------------------------------------------------------------')
print(yanki_df.info())

print(yanki_df.columns)

# Data Cleaning and transformation
# drop missingvalues
yanki_df.dropna(subset=['Order_ID', 'Customer_ID'], inplace=True)
print(yanki_df.info())

# Convert Order_date from string to datetime object
yanki_df['Order_Date'] =pd.to_datetime(yanki_df['Order_Date'], dayfirst=True)
print(yanki_df.info())

#customer_df
customer_df = yanki_df[['Customer_ID', 'Customer_Name', 'Email', 
                        'Phone_Number']].copy().drop_duplicates().reset_index(drop=True)
print(customer_df.head())

#product_table
product_df = yanki_df[['Product_ID','Product_Name', 'Brand', 
                       'Category', 'Price',]].copy().drop_duplicates().reset_index(drop=True )
print(product_df.head())

# shipping  address table
shipping_address_df = yanki_df[['Customer_ID', 'Shipping_Address', 'City', 'State', 
                            'Country', 'Postal_Code']].copy().drop_duplicates().reset_index(drop=True )

shipping_address_df.index.name = 'shipping_ID'
shipping_address_df = shipping_address_df.reset_index()
print(shipping_address_df.head())


# Order table
order_df = yanki_df[['Order_ID', 'Customer_ID', 'Product_ID',
                      'Quantity', 'Total_Price','Order_Date']].copy().drop_duplicates().reset_index(drop=True)
print(order_df.head())

# payment table
payment_method_df = yanki_df[['Order_ID', 'Payment_Method','Transaction_Status']].copy().drop_duplicates().reset_index(drop=True)
print(payment_method_df.head())

# Save the tables to CSV
customer_df.to_csv('dataset\cleaned_data\customers.csv', index=False)
product_df.to_csv('dataset\cleaned_data\products.csv', index=False)
order_df.to_csv('dataset\cleaned_data\orders.csv', index=False)
shipping_address_df.to_csv('dataset\cleaned_data\shipping_address.csv', index=False)
payment_method_df.to_csv('dataset\cleaned_data\payment_method.csv', index=False)

print('---------------------------------------------------------------------')
print(order_df.columns)
print(order_df.info())

import psycopg2

## Data loading
def get_db_connection():
    connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
    return connection

conn = get_db_connection()


# Create SQl tables
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    create_table_query = '''
                          CREATE SCHEMA IF NOT EXISTS yanki;
                          DROP TABLE IF EXISTS yanki.customers CASCADE; 
                          DROP TABLE IF EXISTS yanki.products CASCADE;  
                          DROP TABLE IF EXISTS yanki.shipping_address CASCADE;  
                          DROP TABLE IF EXISTS yanki.orders CASCADE;  
                          DROP TABLE IF EXISTS yanki.payment_method CASCADE;  

                          CREATE TABLE IF NOT EXISTS yanki.customers (
                            Customer_ID UUID PRIMARY KEY,
                            Customer_Name TEXT,
                            Email TEXT,
                            Phone_Number TEXT
                          );

                          CREATE TABLE IF NOT EXISTS yanki.products (
                            Product_ID UUID PRIMARY KEY,
                            Product_Name TEXT,
                            Brand TEXT,
                            Category TEXT,
                            Price FLOAT
                          );

                          
                          CREATE TABLE IF NOT EXISTS yanki.shipping_address (
                            shipping_ID SERIAL PRIMARY KEY,
                            Customer_ID  UUID, 
                            Shipping_Address TEXT,
                            City  TEXT,
                            State  TEXT,
                            Country TEXT,
                            Postal_Code INTEGER,
                            FOREIGN KEY (Customer_ID) REFERENCES yanki.customers(Customer_ID)

                          );

                          CREATE TABLE IF NOT EXISTS yanki.orders (
                            Order_ID UUID PRIMARY KEY,
                            Customer_ID UUID,
                            Product_ID UUID,
                            Quantity INTEGER,
                            Total_Price FLOAT,
                            Order_Date DATE,
                            FOREIGN KEY (Customer_ID) REFERENCES yanki.customers(Customer_ID),
                            FOREIGN KEY (Product_ID) REFERENCES yanki.products(Product_ID)
                          );


                          CREATE TABLE IF NOT EXISTS yanki.payment_method (
                            Order_ID UUID,
                            Payment_Method TEXT,
                            Transaction_Status  TEXT,
                            FOREIGN KEY (Order_ID) REFERENCES yanki.orders(Order_ID)
                          ); '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    
create_table()

##loading data inro tables in postgres
import csv
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r')  as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''
                           INSERT INTO yanki.customers (Customer_ID, Customer_Name, Email, Phone_Number)
                           VALUES(%s, %s, %s, %s);''',
                           row
                            )
    conn.commit()
    cursor.close()
    conn.close()

csv_file_path = r'dataset\cleaned_data\customers.csv'


load_data_from_csv(csv_file_path)

# load products data
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r')  as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''
                           INSERT INTO yanki.products (Product_ID, Product_Name, Brand, Category, Price)
                           VALUES(%s, %s, %s, %s, %s);''',
                           row
                            )
    conn.commit()
    cursor.close()
    conn.close()

csv_file_path = r'dataset\cleaned_data\products.csv'

load_data_from_csv(csv_file_path)


# load shipping address
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r')  as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''
                           INSERT INTO yanki.shipping_address (shipping_ID, Customer_ID, Shipping_Address, City, State, Country,Postal_Code)
                           VALUES(%s, %s, %s, %s, %s, %s, %s);''',
                           row
                            )
    conn.commit()
    cursor.close()
    conn.close()

csv_file_path = r'dataset\cleaned_data\shipping_address.csv'

load_data_from_csv(csv_file_path)

# load orders
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r')  as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''
                           INSERT INTO yanki.orders (Order_ID, Customer_ID, Product_ID, Quantity, Total_Price, Order_Date)
                           VALUES(%s, %s, %s, %s, %s, %s);''',
                           row
                            )
    conn.commit()
    cursor.close()
    conn.close()

csv_file_path = r'dataset\cleaned_data\orders.csv'

load_data_from_csv(csv_file_path)

# load payment method
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r')  as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute('''
                           INSERT INTO yanki.payment_method (Order_ID, Payment_Method, Transaction_Status)
                           VALUES(%s, %s, %s);''',
                           row
                            )
    conn.commit()
    cursor.close()
    conn.close()

csv_file_path = r'dataset\cleaned_data\payment_method.csv'

load_data_from_csv(csv_file_path)