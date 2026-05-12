import pandas as pd
import mysql.connector

# Read CSV file
df = pd.read_csv('index_1.csv')

# Get columns from CSV
columns = list(df.columns)

print("Columns:", columns)

try:

    # Connect to MySQL
    connection = mysql.connector.connect(
        host='localhost',
        database='test_db',
        user='root',
        password='Reimagine@123'
    )

    if connection.is_connected():

        cursor = connection.cursor()

        print("Connected to MySQL")

        # -----------------------------------
        # CREATE TABLE
        # -----------------------------------

        column_definitions = []

        for col in columns:
            column_definitions.append(f"`{col}` VARCHAR(255)")

        create_query = f"""
        CREATE TABLE IF NOT EXISTS index_1 (
            {', '.join(column_definitions)}
        )
        """

        print("\nCreating Table...\n")
        print(create_query)

        cursor.execute(create_query)

        print("Table created successfully!")

        # -----------------------------------
        # INSERT DATA
        # -----------------------------------

        placeholders = ', '.join(['%s'] * len(columns))

        column_names = ', '.join([f"`{col}`" for col in columns])

        insert_query = f"""
        INSERT INTO index_1 ({column_names})
        VALUES ({placeholders})
        """

        print("\nInsert Query:\n")
        print(insert_query)

        # Insert all rows
        for _, row in df.iterrows():

            values = tuple(str(value) for value in row)

            cursor.execute(insert_query, values)

        # Save changes
        connection.commit()

        print(f"\n{cursor.rowcount} rows inserted successfully!")

        # -----------------------------------
        # SHOW DATA
        # -----------------------------------

        cursor.execute("SELECT * FROM index_1 LIMIT 10")

        rows = cursor.fetchall()

        print("\nInserted Data:\n")

        for row in rows:
            print(row)

        cursor.close()
        connection.close()

        print("\nMySQL connection closed.")

except mysql.connector.Error as error:

    print("Error:", error)