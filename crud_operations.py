import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

class CRUDOperations:
    def __init__(self, db_manager):
        self.db = db_manager

    def run_query(self, query, params=None):
        """
        Execute the provided query with optional parameters.
        Returns (True, None) if successful, otherwise (False, error).
        """
        try:
            if params:
                self.db.cursor.execute(query, params)
            else:
                self.db.cursor.execute(query)
            self.db.connection.commit()
            return True, None
        except mysql.connector.Error as err:
            return False, err
        except Exception as e:
            return False, e

    def create(self):
        st.markdown(
            "<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Create a New Table</h2>",
            unsafe_allow_html=True,
        )
        table_name = st.text_input("Enter the table name", placeholder="Press Enter to apply")
        column_definitions = st.text_input(
            "Enter column definitions (e.g., id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100))",
            placeholder="Press Enter to apply"
        )
        
        create_button = st.button("Create Table")
        if create_button:
            if not table_name or not column_definitions:
                st.warning("Please provide both table name and column definitions.")
            else:
                query = f"CREATE TABLE {table_name} ({column_definitions})"
                success, error = self.run_query(query)
                if success:
                    st.success(f"Table '{table_name}' created successfully.")
                else:
                    st.error(f"Error while creating table: {error}")

    def read(self):
        st.markdown(
            "<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Read a Table</h2>",
            unsafe_allow_html=True,
        )
        try:
            table_names = self.db.fetch_tables()
            if not table_names:
                st.warning("No tables found in the database.")
                return
            selected_table = st.selectbox("Select a table", table_names)
            if selected_table:
                query = f"SELECT * FROM {selected_table}"
                try:
                    df = pd.read_sql(query, self.db.connection)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error reading data from table '{selected_table}': {e}")
        except Exception as e:
            st.error(f"Error fetching tables: {e}")

    def update(self):
        st.markdown(
            "<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Update a Table</h2>",
            unsafe_allow_html=True,
        )
        try:
            table_names = self.db.fetch_tables()
            if not table_names:
                st.warning("No tables found in the database.")
                return
            selected_table = st.selectbox("Select a table to update", table_names)
            column_names = self.db.fetch_columns(selected_table)
            if not column_names:
                st.warning("No columns found in the selected table.")
                return

            condition_column = st.selectbox("Select column for condition", column_names)
            condition_value = st.text_input(
                f"Enter the condition value for {condition_column}", placeholder="Press Enter to apply"
            )
            update_column = st.selectbox("Select column to update", column_names)
            new_value = st.text_input(f"Enter the new value for {update_column}", placeholder="Press Enter to apply")
            
            update_button = st.button("Update Table")
            if update_button:
                if not condition_value or not new_value:
                    st.warning("Please provide both condition and new value for the update.")
                else:
                    # Use a parameterized query for safety
                    query = f"UPDATE {selected_table} SET {update_column} = %s WHERE {condition_column} = %s"
                    params = (new_value, condition_value)
                    success, error = self.run_query(query, params)
                    if success:
                        st.success(
                            f"Table '{selected_table}' updated successfully where {condition_column} = '{condition_value}'."
                        )
                    else:
                        st.error(f"Error while updating table: {error}")
        except Exception as e:
            st.error(f"Error in update operation: {e}")

    def delete(self):
        st.markdown(
            "<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Delete a Table</h2>",
            unsafe_allow_html=True,
        )
        try:
            table_names = self.db.fetch_tables()
            if not table_names:
                st.warning("No tables found in the database.")
                return
            selected_table = st.selectbox("Select a table to delete from", table_names)
            action = st.selectbox("Choose an action", ["Delete Rows", "Drop Table"])

            if action == "Delete Rows":
                columns = self.db.fetch_columns(selected_table)
                if not columns:
                    st.warning("No columns found in the selected table.")
                    return
                condition_column = st.selectbox(
                    f"Select column for condition to delete rows from '{selected_table}'", columns
                )
                condition_value = st.text_input(
                    f"Enter the value for {condition_column}", placeholder="Press Enter to apply"
                )
                if st.button("Delete Rows"):
                    if not condition_value:
                        st.warning("Please provide a condition value to delete rows.")
                    else:
                        query = f"DELETE FROM {selected_table} WHERE {condition_column} = %s"
                        params = (condition_value,)
                        success, error = self.run_query(query, params)
                        if success:
                            st.success(
                                f"Rows deleted successfully from '{selected_table}' where {condition_column} = '{condition_value}'."
                            )
                        else:
                            st.error(f"Error while deleting rows: {error}")

            elif action == "Drop Table":
                confirm_drop = st.checkbox(f"Are you sure you want to drop the table '{selected_table}'?")
                if confirm_drop and st.button("Drop Table"):
                    query = f"DROP TABLE {selected_table}"
                    success, error = self.run_query(query)
                    if success:
                        st.success(f"Table '{selected_table}' dropped successfully.")
                    else:
                        st.error(f"Error while dropping table: {error}")
        except Exception as e:
            st.error(f"Error in delete operation: {e}")

    def alter(self):
        st.markdown(
            "<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Alter a Table</h2>",
            unsafe_allow_html=True,
        )
        try:
            table_names = self.db.fetch_tables()
            if not table_names:
                st.warning("No tables found in the database.")
                return
            selected_table = st.selectbox("Select a table to alter", table_names)
            action = st.selectbox("Choose an action", ["Add Column", "Modify Column", "Rename Column", "Drop Column"])

            if action == "Add Column":
                column_name = st.text_input("Enter the column name to add")
                column_type = st.selectbox("Choose the column type", ["INT", "FLOAT", "VARCHAR", "DATE", "BOOLEAN"])
                
                if column_type == "VARCHAR":
                    length = st.selectbox("Choose the length for VARCHAR", [50, 100, 255])
                else:
                    length = None
                
                default_clause = ""
                if column_type == "DATE":
                    date_value = st.date_input("Enter the default date (optional)")
                    if date_value:
                        default_clause = f" DEFAULT '{date_value.strftime('%Y-%m-%d')}'"
                
                add_button = st.button("Add Column")
                if add_button:
                    if column_type == "VARCHAR":
                        query = f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {column_type}({length})"
                    else:
                        query = f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {column_type}{default_clause}"
                    success, error = self.run_query(query)
                    if success:
                        st.success(f"Column '{column_name}' added successfully to table '{selected_table}'.")
                    else:
                        st.error(f"Error while adding column: {error}")

            elif action == "Modify Column":
                columns = self.db.fetch_columns(selected_table)
                if not columns:
                    st.warning("No columns found in the selected table.")
                    return
                column_name = st.selectbox("Select the column to modify", columns)
                column_type = st.selectbox("Select the new data type", ["INT", "VARCHAR", "DATE", "FLOAT", "BOOLEAN"])
                
                if column_type == "VARCHAR":
                    length = st.selectbox("Choose the length for VARCHAR", [50, 100, 255])
                    query = f"ALTER TABLE {selected_table} MODIFY COLUMN {column_name} {column_type}({length})"
                elif column_type == "DATE":
                    date_value = st.date_input("Enter the default date (optional)")
                    default_clause = f" DEFAULT '{date_value.strftime('%Y-%m-%d')}'" if date_value else ""
                    query = f"ALTER TABLE {selected_table} MODIFY COLUMN {column_name} {column_type}{default_clause}"
                else:
                    query = f"ALTER TABLE {selected_table} MODIFY COLUMN {column_name} {column_type}"
                
                modify_button = st.button("Modify Column")
                if modify_button:
                    success, error = self.run_query(query)
                    if success:
                        st.success(f"Column '{column_name}' modified successfully in table '{selected_table}'.")
                    else:
                        st.error(f"Error while modifying column: {error}")

            elif action == "Rename Column":
                columns = self.db.fetch_columns(selected_table)
                if not columns:
                    st.warning("No columns found in the selected table.")
                    return
                old_column = st.selectbox("Select the column to rename", columns)
                new_column_name = st.text_input("Enter the new column name")
                rename_button = st.button("Rename Column")
                if rename_button:
                    if not new_column_name:
                        st.warning("Please enter a new column name.")
                    else:
                        query = f"ALTER TABLE {selected_table} RENAME COLUMN {old_column} TO {new_column_name}"
                        success, error = self.run_query(query)
                        if success:
                            st.success(f"Column '{old_column}' renamed to '{new_column_name}' successfully in table '{selected_table}'.")
                        else:
                            st.error(f"Error while renaming column: {error}")

            elif action == "Drop Column":
                columns = self.db.fetch_columns(selected_table)
                if not columns:
                    st.warning("No columns found in the selected table.")
                    return
                column_name = st.selectbox("Select the column to drop", columns)
                drop_button = st.button("Drop Column")
                if drop_button:
                    query = f"ALTER TABLE {selected_table} DROP COLUMN {column_name}"
                    success, error = self.run_query(query)
                    if success:
                        st.success(f"Column '{column_name}' dropped successfully from table '{selected_table}'.")
                    else:
                        st.error(f"Error while dropping column: {error}")
        except Exception as e:
            st.error(f"Error in alter operation: {e}")









