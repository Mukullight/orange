import sqlite3
import json

db_path = "db.sqlite3"
def dump_sqlite_to_json(db_path, output_file):
    # Connect to the SQLite3 database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Dictionary to hold all table data
    data = {}

    # Iterate over each table
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a list of dictionaries
        table_data = []
        for row in rows:
            table_data.append(dict(zip(column_names, row)))

        # Add table data to the dictionary
        data[table_name] = table_data

    # Close the database connection
    conn.close()

    # Write the data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
#db_path = 'path/to/your/database.db'  # Replace with your database path
output_file = 'output.json'  # Replace with your desired output file path
dump_sqlite_to_json(db_path, output_file)
