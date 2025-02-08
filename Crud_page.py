
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd  # Import pandas here

# MySQL Database Connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="Sushil46",  
            database="zomato"  
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None
    
# Fetch Column Names
def get_column_names(table_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]
        connection.close()
        return column_names
    else:
        return []
    
def get_column_type(table_name, column_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name} WHERE Field = '{column_name}'")
        column = cursor.fetchone()
        connection.close()
        return column[1] if column else None
    return None

# Create Table
def create():
    st.markdown("<h2 style='color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Create a New Table</h2>", unsafe_allow_html=True)
    table_name = st.text_input("Enter the table name", placeholder="Press Enter to apply")
    column_definitions = st.text_input(
        "Enter column definitions (e.g., id VARCHAR(255) PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100))",
        placeholder="Press Enter to apply"
    )
    
    # Button behavior
    create_button = st.button("Create Table")
    if create_button:
        if not table_name or not column_definitions:
            st.warning("Please provide both table name and column definitions.")
        else:
            try:
                connection = create_connection()
                if connection:
                    cursor = connection.cursor()
                    query = f"CREATE TABLE {table_name} ({column_definitions})"
                    cursor.execute(query)
                    connection.commit()
                    st.success(f"Table {table_name} created successfully")
            except Error as e:
                st.error(f"Error while creating table: {e}")
            finally:
                if connection:
                    connection.close()

def read():
    st.markdown("<h2 style='color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Read a Table</h2>", unsafe_allow_html=True)
    connection = create_connection()


    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            selected_table = st.selectbox("Select a table", table_names)
            if selected_table:
                query = f"SELECT * FROM {selected_table}"
                df = pd.read_sql_query(query, connection)  
                st.dataframe(df, use_container_width=True)            
        except Exception as e:
            st.error(f"Error loading data: {e}")
        finally:
            connection.close()

# Update Table
def update():
    st.markdown("<h2 style='color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Update a Table</h2>", unsafe_allow_html=True)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        selected_table = st.selectbox("Select a table to update", table_names)
        
        # Display columns for condition
        column_names = get_column_names(selected_table)
        condition_column = st.selectbox("Select column for condition", column_names)
        
        # Enter condition value
        condition_value = st.text_input(f"Enter the condition value for {condition_column}", placeholder="Press Enter to apply")
        
        # Display columns for update
        update_column = st.selectbox("Select column to update", column_names)
        new_value = st.text_input(f"Enter the new value for {update_column}", placeholder="Press Enter to apply")
        
        # Update button
        update_button = st.button("Update Table")
        if update_button:
            if not condition_value or not new_value:
                st.warning("Please provide both condition and value to update.")
            else:
                try:
                    query = f"UPDATE {selected_table} SET {update_column} = %s WHERE {condition_column} = %s"
                    cursor.execute(query, (new_value, condition_value))
                    connection.commit()
                    st.success(f"Column {update_column} updated successfully in table {selected_table} where {condition_column} = {condition_value}.")
                except Error as e:
                    st.error(f"Error while updating table: {e}")
                finally:
                    connection.close()

# Delete Table (Columns or Rows)
def delete():
    st.markdown("<h2 style='color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Delete a Table</h2>", unsafe_allow_html=True)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        selected_table = st.selectbox("Select a table to delete from", table_names)
        
        action = st.selectbox("Choose an action", ["Delete Columns", "Delete Rows", "Drop Table"])
        
        if action == "Delete Columns":
            column_name = st.selectbox(f"Select column for condition to be deleted", get_column_names(selected_table))
            confirm_drop = st.checkbox(f"Are you sure you want to drop the column {column_name} from {selected_table}?")
            if confirm_drop and st.button("Delete Column"):
                try:
                    query = f"ALTER TABLE {selected_table} DROP COLUMN {column_name}"
                    cursor.execute(query)
                    connection.commit()
                    st.success(f"Column {column_name} dropped successfully from {selected_table}.")
                except Error as e:
                    st.error(f"Error while dropping column: {e}")
        
        elif action == "Delete Rows":
            condition_column = st.selectbox(f"Select column for condition to delete", get_column_names(selected_table))
            condition_value = st.text_input(f"Enter the value for {condition_column}", placeholder="Press Enter to apply")
            if st.button("Delete Rows"):
                if not condition_value:
                    st.warning("Please provide the condition to delete rows.")
                else:
                    try:
                       query = f"DELETE FROM {selected_table} WHERE {condition_column} = %s" 
                       cursor.execute(query, (condition_value,))
                       connection.commit()
                       st.success(f"Row deleted successfully from {selected_table} where {condition_column} = {condition_value}.")
                    except Error as e:
                        st.error(f"Error while deleting rows: {e}")
        
        elif action == "Drop Table":
            confirm_drop = st.checkbox(f"Are you sure you want to drop the table {selected_table}?")
            if confirm_drop and st.button("Drop Table"):
                try:
                    query = f"DROP TABLE {selected_table}"
                    cursor.execute(query)
                    connection.commit()
                    st.success(f"Table {selected_table} dropped successfully.")
                except Error as e:
                    st.error(f"Error while dropping table: {e}")
        connection.close()

# Alter Table
def alter():
    st.markdown("<h2 style='color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Alter a Table</h2>", unsafe_allow_html=True)
    connection = create_connection()

    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        connection.close()

    selected_table = st.selectbox("Select a table to alter", table_names)
    action = st.selectbox("Choose an action", ["Add Column", "Modify Column", "Rename Column", "Drop Column"])

    if action == "Add Column":
        column_name = st.text_input("Enter the column name to add")
        column_type = st.selectbox("Choose the column type", ["INT", "FLOAT", "VARCHAR", "DATE", "BOOLEAN"])
        
        if column_type == "VARCHAR":
            length = st.selectbox("Choose the length for VARCHAR", [50, 100, 255])
        else:
            length = None
        
        if column_type == "DATE":
            date_value = st.date_input("Enter the default date (optional)")
            default_date = f" DEFAULT '{date_value.strftime('%Y-%m-%d')}'" if date_value else ""
        else:
            default_date = ""

        add_button = st.button("Add Column")
        if add_button:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                if column_type == "VARCHAR":
                    cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {column_type}({length})")
                else:
                    cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {column_type}{default_date}")
                    connection.commit()
                st.success(f"Column '{column_name}' added to table '{selected_table}'")
            except Exception as e:
                st.error(f"Error adding column: {e}")

    elif action == "Modify Column":
        column_name = st.selectbox("Select the column to modify", get_column_names(selected_table))
        new_type = st.selectbox("Select the new data type", ["INT", "FLOAT", "VARCHAR", "DATE", "BOOLEAN"])

        if new_type == "VARCHAR":
            length = st.selectbox("Choose the length for VARCHAR", [50, 100, 255])
        elif new_type == "DATE":
            date_value = st.date_input("Enter the default date (optional)")
            default_date = f" DEFAULT '{date_value.strftime('%Y-%m-%d')}'" if date_value else ""
        else:
            length = None
            default_date = ""

        modify_button = st.button("Modify Column")
        if modify_button:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                if new_type == "VARCHAR":
                    cursor.execute(f"ALTER TABLE {selected_table} MODIFY COLUMN {column_name} {new_type}({length})")
                else:
                    cursor.execute(f"ALTER TABLE {selected_table} MODIFY COLUMN {column_name} {new_type}{default_date}")
                    connection.commit()
                st.success(f"Column '{column_name}' modified in table '{selected_table}'")
            except Exception as e:
                st.error(f"Error modifying column: {e}")

    elif action == "Rename Column":
        column_name = st.selectbox("Select the column to rename", get_column_names(selected_table))
        new_column_name = st.text_input("Enter the new column name")

        rename_button = st.button("Rename Column")
        if rename_button:
            try:
                column_type = get_column_type(selected_table, column_name)
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(f"ALTER TABLE {selected_table} CHANGE COLUMN {column_name} {new_column_name} {column_type}")
                connection.commit()
                st.success(f"Column '{column_name}' renamed to '{new_column_name}' in table '{selected_table}'")
            except Exception as e:
                st.error(f"Error renaming column: {e}")

    elif action == "Drop Column":
        column_name = st.selectbox("Select the column to drop", get_column_names(selected_table))
        confirm_drop = st.checkbox(f"Confirm dropping '{column_name}' from {selected_table}")

        drop_button = st.button("Drop Column")
        if drop_button and confirm_drop:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {column_name}")
                connection.commit()
                st.success(f"Column '{column_name}' dropped from table '{selected_table}'")
            except Exception as e:
                st.error(f"Error dropping column: {e}")



# Main Function
def main():

    st.sidebar.markdown("<h2 style='color:#90EE90; text-shadow: 0px 0px 10px #90EE90;'>CRUD Operations</h2streamlit run >", unsafe_allow_html=True)
    page = st.sidebar.selectbox("Choose an action", ["Create", "Read", "Update", "Delete", "Alter"])
    
    if page == "Create":
        create()
    elif page == "Read":
        read()
    elif page == "Update":
        update()
    elif page == "Delete":
        delete()
    elif page == "Alter":
        alter()

if __name__ == "__main__":
    main()
