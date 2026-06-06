# Importing necessary libraries
import numpy as np
import pandas as pd

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
shipping_address_df = yanki_df[['Shipping_Address', 'City', 'State', 
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


