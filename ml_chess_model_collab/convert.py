import sqlite3
import csv
import os

def convert_db_to_csv(db_file, table_name, csv_file):
    # Convert relative paths to absolute paths
    db_file = os.path.abspath(db_file)
    csv_file = os.path.abspath(csv_file)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Fetch all data from the specified table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 100000")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the column names as the first row
        writer.writerow(column_names)
        # Write all the rows
        writer.writerows(rows)
    
    # Close the database connection
    conn.close()

    print(f"Data from {table_name} table in {db_file} has been written to {csv_file}")

convert_db_to_csv('./test.db', 'evaluations', 'evals_mock.csv')
