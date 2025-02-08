import streamlit as st
import mysql.connector
import pandas as pd

class ClassApp:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.selected_table = None
        self.df = None

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sushil46",
                database="zomato"
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            st.error(f"Error connecting to MySQL: {err}")
            st.stop()

    def fetch_table_names(self):
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            st.error(f"Error fetching tables: {e}")
            return []

    def fetch_data_from_selected_table(self):
        if self.selected_table:
            try:
                query = f"SELECT * FROM {self.selected_table}"
                self.df = pd.read_sql_query(query, self.connection)
            except Exception as e:
                st.error(f"Error loading data: {e}")

    def display_data(self):
        if self.df is not None:
            st.dataframe(self.df, use_container_width=True)

    def close_database_connection(self):
        if self.connection:
            self.connection.close()

    def run(self):
        st.markdown("<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Zomato Data Analysis</h2>", unsafe_allow_html=True)

        self.connect_to_database()
        table_names = self.fetch_table_names()
        if table_names:
            self.selected_table = st.selectbox("Select a Table", table_names)
            self.fetch_data_from_selected_table()
            self.display_data()
        else:
            st.error("No tables found in the database.")
        self.close_database_connection()

if __name__ == "__main__":
    app = ClassApp()
    app.run()