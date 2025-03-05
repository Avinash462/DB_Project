import pyodbc

# Define database connection parameters (Windows Authentication)
server = 'DESKTOP-ACSF2AH'  # Your SQL Server name
database = 'OFODS-Revised'  # Your database name

try:
    # Establish connection using Windows Authentication
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("Successfully connected to the database using Windows Authentication.\n")

    # QUERY 1: Get total orders per customer (Removing HAVING clause to ensure all customers appear)
    query1 = """
    SELECT C.Customer_ID, C.First_Name, C.Last_Name, COUNT(O.Order_ID) AS Total_Orders
    FROM Customers C
    LEFT JOIN Orders O ON C.Customer_ID = O.Customer_ID
    GROUP BY C.Customer_ID, C.First_Name, C.Last_Name
    ORDER BY Total_Orders DESC;
    """

    # QUERY 2: Get the most ordered menu items (Removing TOP 5 for testing)
    query2 = """
    SELECT MI.Name AS Menu_Item, R.Name AS Restaurant, COUNT(OI.Menu_Item_ID) AS Times_Ordered
    FROM Order_Items OI
    JOIN Menu_Items MI ON OI.Menu_Item_ID = MI.Menu_Item_ID
    JOIN Restaurants R ON MI.Restaurant_ID = R.Restaurant_ID
    GROUP BY MI.Name, R.Name
    ORDER BY Times_Ordered DESC;
    """

    # QUERY 3: Get revenue generated per restaurant (Fixing alias issue)
    query3 = """
    SELECT R.Restaurant_ID, R.Name AS Restaurant_Name, ISNULL(SUM(P.Amount), 0) AS Total_Revenue
    FROM Restaurants R
    LEFT JOIN Menu_Items MI ON R.Restaurant_ID = MI.Restaurant_ID
    LEFT JOIN Order_Items OI ON MI.Menu_Item_ID = OI.Menu_Item_ID
    LEFT JOIN Orders O ON OI.Order_ID = O.Order_ID
    LEFT JOIN Payments P ON O.Order_ID = P.Order_ID
    GROUP BY R.Restaurant_ID, R.Name
    ORDER BY Total_Revenue DESC;
    """

    # Execute queries
    cursor.execute(query1)
    results1 = cursor.fetchall()

    cursor.execute(query2)
    results2 = cursor.fetchall()

    cursor.execute(query3)
    results3 = cursor.fetchall()

    # Define output file
    output_file = "Report.txt"

    # Open the file to write results
    with open(output_file, "w", encoding="utf-8") as file:
        # Print & Write Query 1 Results
        print("\nTotal Orders Per Customer")
        file.write("Total Orders Per Customer\n")
        file.write("Customer_ID | First_Name | Last_Name | Total_Orders\n")
        file.write("-" * 60 + "\n")
        if results1:
            for row in results1:
                line = f"{row[0]} | {row[1]} | {row[2]} | {row[3]}"
                print(line)  # Print to terminal
                file.write(line + "\n")  # Write to file
        else:
            print("No data found for Total Orders Per Customer.")
            file.write("No data found.\n")

        print("\n")  # Add spacing between sections
        file.write("\n\n")

        # Print & Write Query 2 Results
        print("Most Ordered Menu Items")
        file.write("Most Ordered Menu Items\n")
        file.write("Menu_Item | Restaurant | Times_Ordered\n")
        file.write("-" * 60 + "\n")
        if results2:
            for row in results2:
                line = f"{row[0]} | {row[1]} | {row[2]}"
                print(line)
                file.write(line + "\n")
        else:
            print("No data found for Most Ordered Menu Items.")
            file.write("No data found.\n")

        print("\n")  # Add spacing between sections
        file.write("\n\n")

        # Print & Write Query 3 Results
        print("Revenue Generated Per Restaurant")
        file.write("Revenue Generated Per Restaurant\n")
        file.write("Restaurant_ID | Restaurant_Name | Total_Revenue\n")
        file.write("-" * 60 + "\n")
        if results3:
            for row in results3:
                line = f"{row[0]} | {row[1]} | ${row[2]:.2f}"
                print(line)
                file.write(line + "\n")
        else:
            print("No data found for Revenue Generated Per Restaurant.")
            file.write("No data found.\n")

    print(f"\nComplex Reports successfully saved to {output_file}")

except pyodbc.Error as e:
    print(f"Database Error: {e}")

except Exception as e:
    print(f"Unexpected Error: {e}")

finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")
