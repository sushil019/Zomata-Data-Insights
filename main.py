import streamlit as st
from App_pages import ClassApp
from Queries_page import ZomatoQueries
from PIL import Image

class ClassIntroduction:
    def __init__(self):
        self.page = None
        self.operation = None

    def setup_sidebar(self):
        st.sidebar.markdown("<h2 style='font-family: Copperplate; color:#90EE90; text-shadow: 0px 0px 10px #90EE90;'>Navigation</h2>", unsafe_allow_html=True)
        self.page = st.sidebar.selectbox("Go to:", ["Introduction", "App", "CRUD", "Queries"])

        st.sidebar.markdown("---")

        if self.page == "CRUD":
            st.sidebar.markdown("<h2 style='font-family: Copperplate; color:#90EE90; text-shadow: 0px 0px 10px #90EE90;'>CRUD Operations</h2>", unsafe_allow_html=True)
            self.operation = st.sidebar.selectbox("Select an Operation", ["Create", "Read", "Update", "Delete", "Alter"], key="crud_select")
            st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    def introduction_page(self):
        # Title with Copperplate font
        st.markdown("<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>Zomato - Food Delivery Data Insights Using Python and SQL</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Layout for left and right columns
        left, right = st.columns([3, 1])  
        with left:
            st.markdown("""
                <p style='font-family: Bradley Hand; color:#FFFFFF; font-size:18px; text-align:left; line-height:1.6;'>
                In this project, we are going to scrape and analyze Zomato's food delivery data using Python (Faker) and SQL. 
                Our analysis aims to cover scraping data insights of Zomato's operations and improve customer satisfaction by 
                analyzing food delivery data by customer preferences, delivery times, and more. Furthermore, this project 
                demonstrates the integration of Streamlit for visualizing the results interactively.
                </p>
                """, unsafe_allow_html=True)

        with right:
            zomato_image = Image.open("Zomato.png")
            st.image(zomato_image, use_column_width=True)

        # Highlights Section
        st.markdown("<h3 style='font-family: Copperplate; color:#ce93d8; text-shadow: 0px 0px 10px #ebaef5;'>Highlights:</h3>", unsafe_allow_html=True)
        st.markdown("""
            <p style='font-family: Bradley Hand; color:#FFFFFF; font-size:18px; text-align:left;'>
            - How we scraped Zomato data<br>
            - Data preprocessing and cleaning<br>
            - SQL-based analysis for trends and insights<br>
            - Building an interactive web app using Streamlit
            </p>
            """, unsafe_allow_html=True)

        # Skills and Takeaways Section
        st.markdown("<h3 style='font-family: Copperplate; color:#ce93d8; text-shadow: 0px 0px 10px #ebaef5;'>Skills and Takeaways:</h3>", unsafe_allow_html=True)
        st.markdown("""
            <p style='font-family: Bradley Hand; color:#FFFFFF; font-size:18px; text-align:left;'>
            - SQL<br>
            - Python<br>
            - Streamlit<br>
            - Data Engineering<br>
            - Database Management
            </p>
            """, unsafe_allow_html=True)

        # Applying the glow effect on the "Submitted By" text
        st.markdown("<div style='font-family: Bradley Hand; color:#00FF33; font-size:16px; text-align:right; text-shadow: 0px 0px 15px #00FF33;'>Submitted By: Sushil Kumar K</div>", unsafe_allow_html=True)

    def app_page(self):
        app = ClassApp()
        app.run()

    def queries_page(self):
        queries = ZomatoQueries()
        queries.display_query_results()

    def main(self):
        self.setup_sidebar()

        if self.page == "Introduction":
            self.introduction_page()
        elif self.page == "App":
            self.app_page()
        elif self.page == "Queries":
            self.queries_page()

if __name__ == "__main__":
    app = ClassIntroduction()
    app.main()








