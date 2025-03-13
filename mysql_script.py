import mysql.connector  # Importing the MySQL connector for Python, allowing connection to the MySQL database

try:
    print("Fetching data from MySQL...")  # Indicating the start of the data fetching process

    # Connecting to MySQL Database
    conn = mysql.connector.connect(
        host="localhost",  # Hostname where the MySQL server is running
        user="root",  # MySQL username
        password="NewSecurePassword",  # MySQL password
        database="olist_ecommerce"  # Database name to connect to
    )

    # Creating a cursor object to execute queries
    cursor = conn.cursor()

    # SQL Query to retrieve data from the database
    query = """
    SELECT c.order_id, 
           COALESCE(cu.customer_city, g.geolocation_city, 'Unknown City') AS customer_city,  # Get customer city, fallback to geolocation city or 'Unknown City' if missing
           c.order_status,  # Get order status
           COUNT(DISTINCT o.order_item_id) AS total_items,  # Count distinct order items to prevent duplicate counting
           COALESCE(SUM(DISTINCT p.payment_value), SUM(o.price + o.freight_value), 0.00) AS total_payment  # Calculate total payment, fallback to price + freight value if payment value is missing
    FROM customer_order_summary c  # Main table containing order data
    LEFT JOIN customers cu ON c.customer_id = cu.customer_id  # Join with customers table based on customer_id
    LEFT JOIN geolocation g ON cu.customer_zip_code_prefix = g.geolocation_zip_code_prefix  # Join with geolocation table based on zip code prefix
    LEFT JOIN order_items o ON c.order_id = o.order_id  # Join with order_items table to get order items
    LEFT JOIN order_payments p ON c.order_id = p.order_id  # Join with order_payments table to get payment details
    GROUP BY c.order_id, customer_city, c.order_status  # Group results by order_id, customer city, and order status
    LIMIT 3;  # Limit the result to the first 3 rows for preview
    """

    # Executing the SQL query
    cursor.execute(query)
    # Fetching all the results of the query
    results = cursor.fetchall()

    # Writing the results to a text file
    with open("order_report.txt", "w") as file:
        # Write the header to the file
        file.write("Customer Order Report\n\n")
        # Loop through each row of the results and write it to the file
        for row in results:
            file.write(f"Order ID: {row[0]}\n")  # Writing Order ID
            file.write(f"Customer City: {row[1]}\n")  # Writing Customer City
            file.write(f"Order Status: {row[2]}\n")  # Writing Order Status
            file.write(f"Total Items: {row[3]}\n")  # Writing Total Items

            # Fix for NULL payments in Python: If total_payment is None, replace it with 0.00
            total_payment = row[4] if row[4] is not None else 0.00
            file.write(f"Total Payment: ${total_payment:.2f}\n")  # Writing Total Payment formatted to two decimal places
            file.write("-" * 30 + "\n")  # Separating each order by 30 dashes

    print("Report Generated: order_report.txt")  # Indicating that the report has been successfully generated

except mysql.connector.Error as err:  # Catching any errors that occur during the database connection or query execution
    print(f"Error: {err}")  # Displaying the error message

finally:
    # Ensuring the connection is closed properly
    if 'conn' in locals() and conn.is_connected():
        conn.close()  # Closing the connection
        print("🔌 Connection Closed.")  # Indicating that the connection has been closed
