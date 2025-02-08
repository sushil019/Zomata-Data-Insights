import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error: {e}")

    def fetch_tables(self):
        """Fetch all table names in the database."""
        try:
            self.cursor.execute("SHOW TABLES")
            return [table[0] for table in self.cursor.fetchall()]
        except Error as e:
            print(f"Error fetching tables: {e}")
            return None

    def fetch_columns(self, table_name):
        """Fetch column names of a given table."""
        try:
            self.cursor.execute(f"DESCRIBE {table_name}")
            return [row[0] for row in self.cursor.fetchall()]
        except Error as e:
            print(f"Error fetching columns: {e}")
            return None

    def execute_query(self, query):
        """Execute a given SQL query."""
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Error executing query: {e}")

    def fetch_data(self, query):
        """Fetch data from the database using a provided query."""
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()











