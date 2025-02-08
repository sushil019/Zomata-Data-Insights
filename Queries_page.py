# zomato_queries_page.py
import streamlit as st
import pandas as pd
import mysql.connector as mysql

class ZomatoQueries:
    def __init__(self):
        self.sql_queries = {
            "1": "SELECT COUNT(*) AS total_premium_customers FROM zomato.customers WHERE is_premium = TRUE;",
            "2": "SELECT customer_id, payment_mode FROM zomato.orders WHERE payment_mode = 'Cash';",
            "3": "SELECT CASE WHEN HOUR(delivery_time) < 12 THEN 'Morning' ELSE 'Evening' END AS orders_placed, COUNT(*) AS total_orders FROM zomato.orders GROUP BY orders_placed ORDER BY total_orders DESC;",
            "4": "SELECT delivery_person_id, name, average_rating FROM zomato.delivery_persons WHERE average_rating > 4.0;",
            "5": "SELECT restaurant_id, COUNT(order_id) AS total_orders FROM zomato.orders WHERE YEAR(order_date) = 2025 GROUP BY restaurant_id HAVING total_orders > 10;",
            "6": "SELECT order_id, customer_id, total_amount, discount_applied FROM zomato.orders WHERE discount_applied > 100;",
            "7": "SELECT customer_id, name, is_premium FROM zomato.customers WHERE is_premium = TRUE;",
            "8": "SELECT delivery_person_id, COUNT(*) AS total_deliveries FROM zomato.deliveries GROUP BY delivery_person_id ORDER BY total_deliveries DESC LIMIT 5;",
            "9": "SELECT delivery_person_id, COUNT(*) AS total_deliveries FROM zomato.deliveries GROUP BY delivery_person_id ORDER BY total_deliveries ASC LIMIT 5;",
            "10": "SELECT restaurant_id, SUM(total_amount) AS revenue FROM zomato.orders GROUP BY restaurant_id ORDER BY revenue DESC LIMIT 5;",
            "11": "SELECT customer_id, COUNT(order_id) AS total_orders FROM zomato.orders GROUP BY customer_id ORDER BY total_orders DESC LIMIT 5;",
            "12": "SELECT customer_id, SUM(total_amount) AS total_spent FROM zomato.orders GROUP BY customer_id ORDER BY total_spent DESC LIMIT 5;",
            "13": "SELECT customer_id, COUNT(order_id) AS total_orders FROM zomato.orders WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY customer_id;",
            "14": "SELECT restaurant_id, `average_delivery_time(min)` FROM zomato.restaurants WHERE `average_delivery_time(min)` < 30;",
            "15": "SELECT vehicle_type, SUM(delivery_fee) AS total_delivery_fee FROM zomato.deliveries GROUP BY vehicle_type;",
            "16": "SELECT customer_id, name, total_orders FROM customers WHERE total_orders > 5;",
            "17": "SELECT restaurant_id, is_active, `average_delivery_time(min)` FROM zomato.restaurants WHERE is_active = True;",
            "18": "SELECT cuisine_type, SUM(total_orders) AS total_orders FROM zomato.restaurants GROUP BY cuisine_type ORDER BY total_orders DESC LIMIT 1;",
            "19": "SELECT customer_id, status FROM zomato.orders WHERE status = 'Cancelled';",
            "20": "SELECT customer_id, name, signup_date FROM zomato.customers WHERE YEAR(signup_date) = 2024;"
        }

        self.query_titles = [
            "1. Total number of premium customers",
            "2. Customers Who Used Cash as Payment Mode",
            "3. Peak timing when most orders are placed",
            "4. Delivery persons with an average rating above 4.0",
            "5. Restaurants that delivered more than 10 orders in 2025",
            "6. Orders with a discount applied greater than 100%",
            "7. Customers who placed premium orders",
            "8. Top 5 delivery persons with the most deliveries",
            "9. Least 5 delivery persons with the least deliveries",
            "10. Top 5 restaurants by revenue",
            "11. Top 5 customers with maximum orders",
            "12. Top 5 spending customers",
            "13. Customers who placed orders in 2025",
            "14. Restaurants with an average delivery time of less than 30 minutes",
            "15. Total delivery fee collected by vehicle type",
            "16. Customers with more than 5 orders",
            "17. Average delivery time of active restaurants",
            "18. Most popular cuisine type",
            "19. Canceled orders by the customers",
            "20. Customers who signed up in 2024"
        ]

    def create_connection(self):
        return mysql.connect(
            user='root',
            password='Sushil46',
            host='localhost',
            database='zomato'
        )

    def execute_query(self, query_key):
        try:
            connection = self.create_connection()
            cursor = connection.cursor()
            query = self.sql_queries[query_key]
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if data:
                df = pd.DataFrame(data, columns=columns)
                return df
            else:
                return None
        except mysql.Error as err:
            st.error(f"Error: {err}")
        finally:
            connection.close()

    def display_query_results(self):
        st.markdown("<h2 style='font-family: Copperplate; color:#16E2F5; text-shadow: 0px 0px 10px #16E2F5;'>QUERIES</h2>", unsafe_allow_html=True)

        selected_index = st.selectbox("Select a query", self.query_titles)

        # Extract the corresponding query key
        query_key = str(self.query_titles.index(selected_index) + 1)

        # Execute the selected query and display results
        if query_key:
            result_df = self.execute_query(query_key)
            if result_df is not None:
                st.dataframe(result_df)
            else:
                st.info("No data available for this query.")


# Main function to run the app
def main():
    zomato_app = ZomatoQueries()
    zomato_app.display_query_results()

if __name__ == "__main__":
    main()

