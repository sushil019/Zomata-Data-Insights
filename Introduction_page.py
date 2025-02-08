import streamlit as st
from PIL import Image
import mysql.connector
import pandas as pd

class ClassIntroduction:
    def __init__(self):
        self.page = None
        self.operation = None

    def set_page_config(self):
        st.set_page_config(page_title="Zomato Data Insights", layout="wide")

    def set_css(self):
        st.markdown(
            """
            <style>
            .main-title {
                font-family: 'Arial Rounded MT Bold';
                font-size: 40px;
                text-align: center;
                color: #16E2F5;
                text-shadow: 0px 0px 10px #16E2F5;
                margin-bottom: 20px;
            }
            .details {
                font-family: 'Bradley Hand', cursive;
                color: #FFFFFF ;
                text-align: center;
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            .highlights-title, .skills-title {
                font-family: 'Copperplate', serif;
                color: #ce93d8;
                font-size: 24px;
                margin-top: 20px;
            }
            .bullet-points {
                font-family: 'Bradley Hand', cursive;
                color: #FFFFFF ;
                font-size: 18px;
                margin-left: 20px;
                line-height: 1.8;
            }
            .submitted {
                font-family: 'Bradley Hand', cursive;
                color: #00FF33;
                font-size: 16px;
                text-align: right;
                margin-top: 20px;
            }
            .image-container {
                display: flex;
                justify-content: flex-end;
                align-items: flex-start;
            }
            .subtitle {
                font-family: 'Arial Rounded MT Bold';
                font-size: 20px;
                text-align: left;
                color: lightgreen;
                margin-bottom: 10px;
                text-shadow: 0px 0px 5px lightgreen;
            }
            .spaced {
                margin-top: 30px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def setup_sidebar(self):
        st.sidebar.title("Navigation")
        self.page = st.sidebar.selectbox("Go to:", ["Introduction","App", "CRUD", "Queries"])

        st.sidebar.markdown("---")
        st.sidebar.markdown("")

        if self.page == "CRUD":
            st.sidebar.markdown("<div class='subtitle'>CRUD Operations</div>", unsafe_allow_html=True)
            self.operation = st.sidebar.selectbox("Select an Operation", ["Create", "Read", "Update", "Delete", "Alter"], key="crud_select")
            st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    def introduction_page(self):
        st.markdown("<div class='main-title'>Zomato - Food Delivery Data Insights Using Python and SQL</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns([3, 1])  # Adjust column widths
        with left:
            st.markdown(
                """
                <div class='details'>
                In this project, we are going to scrape and analyze Zomato's food delivery data using Python (Faker) and SQL. 
                Our analysis aims to cover scraping data insights of Zomato operation and improve customer satisfaction by 
                analyzing food delivery data by customer preferences, delivery times, and more. Furthermore, this project 
                demonstrates the integration of Streamlit for visualizing the results interactively.
                </div>
                """,
                unsafe_allow_html=True
            )
        with right:
            zomato_image = Image.open("Zomato.png")
            st.image(zomato_image, use_container_width=True)

        st.markdown("<div class='highlights-title'>Highlights:</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='bullet-points'>
            - How we scraped Zomato data<br>
            - Data preprocessing and cleaning<br>
            - SQL-based analysis for trends and insights<br>
            - Building an interactive web app using Streamlit<br>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div class='skills-title'>Skills and Takeaways:</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='bullet-points'>
            - SQL<br>
            - Python<br>
            - Streamlit<br>
            - Data Engineering<br>
            - Database Management<br>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div class='submitted'>Submitted By: Sushil Kumar K</div>", unsafe_allow_html=True)

    def main(self):
        self.set_page_config()
        self.set_css()
        self.setup_sidebar()

        if self.page == "Introduction":
            self.introduction_page()

if __name__ == "__main__":
    class_introduction = ClassIntroduction()
    class_introduction.main()

