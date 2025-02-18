import pandas as pd
import json
import xmltodict

# Function to convert CSV to SQL INSERT statements
def csv_to_sql(file_path, table_name, columns):
    df = pd.read_csv(file_path)
    sql_statements = []
    for _, row in df.iterrows():
        values = "', '".join(str(row[col]) for col in columns)
        sql_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ('{values}');")
    return sql_statements

# Function to convert JSON to SQL INSERT statements
def json_to_sql(file_path, table_name, columns):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    sql_statements = []
    for entry in data:
        values = "', '".join(str(entry[col]) for col in columns)
        sql_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ('{values}');")
    return sql_statements

# Function to convert XML to SQL INSERT statements
def xml_to_sql(file_path, table_name, columns):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = xmltodict.parse(f.read())
    sql_statements = []
    for entry in data['payments']['payment']:
        values = "', '".join(str(entry[col]) for col in columns)
        sql_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ('{values}');")
    return sql_statements

# File paths
files = {
    "Customers": ("customers.csv", ["Customer_ID", "First_Name", "Last_Name", "Email", "Address", "Zip_Code"]),
    "Restaurants": ("restaurants.json", ["Restaurant_ID", "Name", "Cuisine", "Location", "Rating"]),
    "Menu_Items": ("menu_items.csv", ["Menu_Item_ID", "Restaurant_ID", "Name", "Price", "Availability"]),
    "Orders": ("orders.csv", ["Order_ID", "Customer_ID", "Order_Date", "Order_Status", "Total_Cost"]),
    "Payments": ("payments.xml", ["Transaction_ID", "Order_ID", "Amount", "Payment_Method", "Status"]),
    "Delivery_Personnel": ("delivery_personnel.csv", ["Delivery_ID", "Name", "Phone_Number", "Vehicle_Type"]),
    "Reviews_Ratings": ("reviews_ratings.csv", ["Review_ID", "Customer_ID", "Restaurant_ID", "Comments", "Rating"])
}

# Generate SQL Statements
all_sql_statements = []
for table, (file_path, columns) in files.items():
    if file_path.endswith(".csv"):
        all_sql_statements.extend(csv_to_sql(file_path, table, columns))
    elif file_path.endswith(".json"):
        all_sql_statements.extend(json_to_sql(file_path, table, columns))
    elif file_path.endswith(".xml"):
        all_sql_statements.extend(xml_to_sql(file_path, table, columns))

# Save to a file
with open("insert_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(all_sql_statements))

print("SQL INSERT statements saved to insert_data.sql")
