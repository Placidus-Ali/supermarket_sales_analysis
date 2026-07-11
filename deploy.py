import os
import joblib
import pandas as pd
import streamlit as st
from PIL import Image

print("Libraries imported successfully")

# Getting the directory path
script_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the trained Model
model_path = os.path.join(script_dir, "supermarket_sales_rf_model.pkl")
model = joblib.load(model_path)
print("Sales Model Loaded Successfully")

# Loading Image
image_path = os.path.join(script_dir, "sales_forecasting.jfif")
image = Image.open(image_path)
print("Image Loaded Successfully")

# Mapping the encoded columns
branch_lookup = {0: "Alex", 1: "Cairo", 2: "Giza"}
city_lookup = {0: "Mandalay", 1: "Naypyitaw", 2: "Yangon"}
customer_type_lookup = {0: "Member", 1: "Normal"}
gender_lookup = {0: "Female", 1: "Male"}
product_line_lookup = { 0: "Electronic Accessories", 1: "Fashion Accessories", 2: "Food and Beverages", 3: "Health and Beauty", 4: "Home and Lifestyle", 5: "Sports and Travel"}
payment_lookup = {0: "Cash", 1: "Credit Card", 2: "Ewallet"}

# Creating user interface
st.title("Store Sales Model")
st.image(image)
st.write("Enter the store details below to predict the sales revenue:")

# Documentation dropdown
with st.expander("Documentation: Feature Descriptions"):
    st.write("**Branch**: The branch location of the supermarket (e.g., Yangon, Naypyitaw, Mandalay)")
    st.write("**City**: The city in which the supermarket branch is located")
    st.write("**Customer Type**:Indicates whether the customer is a 'Member' or 'Normal'")
    st.write("**Gender**: Gender of the Customer")
    st.write("**Product Line**: The category of the product sold (e.g., Health & Beauty, Electronic Accessories, Home & Lifestyle)")
    st.write("**Unit Price**: Price per unit of the product.")
    st.write("**Quantity**: Number of items purchased")
    st.write("**Payment**: Payment method used (e.g., Cash, Ewallet, Credit card)")
    st.write("**Rating**: Customer satisfaction rating (out of 10)")
    st.write("**Hour**: The time of the day when the transaction happened")
    st.write("**Day Of Week**: The day of the week when the transaction happened. (Monday as 1, Sunday as 6)")
    st.write("**Month**: The month when the transaction happened")
    st.write("**Sales**: The total sales per transaction which is the target variable")


# Initializing sessions to create page by page
if "step" not in st.session_state:
    st.session_state.step = 1

# Step 1 defaults
if "Branch" not in st.session_state: st.session_state.Branch = 0
if "City" not in st.session_state: st.session_state.City = 0
if "Customer_type" not in st.session_state: st.session_state.Customer_type = 0
if "Gender" not in st.session_state: st.session_state.Gender = 0

# Step 2 defaults
if "Product_line" not in st.session_state: st.session_state.Product_line = 0
if "Unit_price" not in st.session_state: st.session_state.Unit_price = 10.00
if "Quantity" not in st.session_state: st.session_state.Quantity = 1
if "Payment" not in st.session_state: st.session_state.Payment = 0

# Step 3 defaults
if "Rating" not in st.session_state: st.session_state.Rating = 4.0
if "Hour" not in st.session_state: st.session_state.Hour = 10
if "DayOfWeek" not in st.session_state: st.session_state.DayOfWeek = 0
if "Month" not in st.session_state: st.session_state.Month = 1


# Progress Bar
st.progress(st.session_state.step / 3)
st.subheader(f"Step {st.session_state.step} of 3")

# Core Store Details
if st.session_state.step == 1:
    st.markdown("### Store & Customer Demographics")
    st.selectbox("Branch", options=[0, 1, 2], format_func=lambda x: branch_lookup[x], key="Branch")
    st.selectbox("City", options=[0, 1, 2], format_func=lambda x: city_lookup[x], key="City")
    st.selectbox("Customer Type", options=[0, 1], format_func=lambda x: customer_type_lookup[x], key="Customer_type")
    st.selectbox("Gender", options=[0, 1], format_func=lambda x: gender_lookup[x], key="Gender")

    if st.button("Next"):
        st.session_state.step = 2
        st.rerun()

# Transaction Details
elif st.session_state.step == 2:
    st.markdown("### Product & Transaction Info")
    st.selectbox("Product Line", options=[0, 1, 2, 3, 4, 5], format_func=lambda x: product_line_lookup[x], key="Product_line")
    st.number_input("Unit Price", min_value=10.00, max_value=100.00, step=0.01, key="Unit_price")
    st.number_input("Quantity", min_value=1, max_value=10, step=1, key="Quantity")
    st.selectbox("Payment", options=[0, 1, 2], format_func=lambda x: payment_lookup[x], key="Payment")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.step = 3
            st.rerun()

# Final Details & Prediction
elif st.session_state.step == 3:
    st.markdown("### Time & Feedback Metrics")
    st.number_input("Rating", min_value=4.0, max_value=10.0, step=0.1, key="Rating")
    st.number_input("Hour", min_value=10, max_value=20, step=1, key="Hour")
    st.number_input("Day Of Week", min_value=0, max_value=6, step=1, key="DayOfWeek")
    st.number_input("Month", min_value=1, max_value=3, step=1, key="Month")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()

    st.markdown("---")
    if st.button("Predict Total Sales"):
        print("Input Features Collected")

        # Organize inputs using st.session_state keys
        input_data = pd.DataFrame(
            [[
                st.session_state.Branch, 
                st.session_state.City, 
                st.session_state.Customer_type, 
                st.session_state.Gender, 
                st.session_state.Product_line, 
                st.session_state.Unit_price, 
                st.session_state.Quantity, 
                st.session_state.Payment, 
                st.session_state.Rating, 
                st.session_state.Hour, 
                st.session_state.DayOfWeek, 
                st.session_state.Month
            ]],
            columns=["Branch", "City", "Customer type", "Gender", "Product line", "Unit price", "Quantity", "Payment", "Rating", "Hour", "DayOfWeek", "Month"])

        prediction = model.predict(input_data)[0]

        # Show Result
        st.success(f"Predicted Sales: **${prediction:,.2f}**")

        # Provide a simple business summary based on the prediction
        if prediction > 15000:
            st.info("**Sales Status:** High-performing day expected! Check inventory levels.")
        elif prediction > 5000:
            st.info("**Sales Status:** Average performance expected.")
        else:
            st.info("**Sales Status:** Low sales volume projected. Consider launching a flash sale.")

print("Sales Prediction Completed Successfully")
