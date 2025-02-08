from database_manager import DatabaseManager
from crud_operations import CRUDOperations
import streamlit as st
from main import ClassIntroduction  

# Initialize DatabaseManager
db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="Sushil46",
    database="zomato"
)

# Initialize CRUDOperations
crud_ops = CRUDOperations(db_manager)

# Initialize the navigation using ClassIntroduction
intro = ClassIntroduction()
intro.setup_sidebar()  # This sets up the sidebar with navigation options and, if "CRUD" is selected, a CRUD operation selector

# Navigation logic based on sidebar selection
if intro.page == "Introduction":
    intro.introduction_page()
elif intro.page == "App":
    intro.app_page()
elif intro.page == "Queries":
    intro.queries_page()
elif intro.page == "CRUD":
    # For CRUD, use the operation selected in the sidebar within the CRUD page
    if intro.operation == "Create":
        crud_ops.create()
    elif intro.operation == "Read":
        crud_ops.read()
    elif intro.operation == "Update":
        crud_ops.update()
    elif intro.operation == "Delete":
        crud_ops.delete()
    elif intro.operation == "Alter":
        crud_ops.alter()









