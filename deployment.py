import streamlit as st
import pandas as pd
import joblib
import os
from PIL import Image
print("Libraries impoerted successfully")

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
Branch = {0: "Alex", 1: "Cairo", 2: "Giza"}   
City =  {0: "Mandalay", 1: "Naypyitaw", 2: "Yangon"}  
Customer_type =  {0: "Member", 1: "Normal"}    
Gender =  {0: "Female", 1: "Male"}  
Product_line = {0: "Electronic Accessories", 1: "Fashion Accessories", 2: "Food and Beverages", 3: "Health and Beauty", 4: "Home and Lifestyle", 5: "Sports and Travel"}  
Payment =  {0: "Cash", 1: "Credit Card", 2: "Ewallet"}




# 5. CREATE THE USER INTERFACE (UI)
st.title("📈 Store Sales Predictor")
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

# 6. COLLECT USER INPUTS
Branch =  st.selectbox("Branch", options=[0, 1, 2], format_func=lambda x: Branch[x])
City = st.selectbox("City", options=[0, 1, 2], format_func=lambda x: City[x])
Customer_Type = st.selectbox("Customer Type", options=[0, 1], format_func=lambda x: Customer_type[x])
Gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: Gender[x])
Product_Line = st.selectbox("Product Line", options=[0, 1, 2, 3, 4, 5], format_func=lambda x: Product_line[x])
Unit_Price = st.number_input("Unit Price", min_value=10.00, max_value=100.00, value=10.00, step=0.01) 
Quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1, step=1) 
Payment = st.selectbox("Payment", options=[0, 1, 2, 3, 4, 5], format_func=lambda x: Product_line[x])
Rating = st.number_input("Rating", min_value=4.0, max_value=10.0, value=4.0, step=0.1) 
Hour = st.number_input("Hour", min_value=10, max_value=20, value=10, step=1) 
DayOfWeek = st.number_input("Day Of Week", min_value=0, max_value=6, value=0, step=1) 
Month = st.number_input("Month", min_value=1, max_value=3, value=1, step=1) 


print('Input Features Collected')

# 7. PREDICTION LOGIC
if st.button("Predict Total Sales"):
    
    # Organize inputs into a pandas DataFrame 
    input_data = pd.DataFrame(
        [[Branch, City, Customer_Type, Gender, Product_line, Unit_Price, Quantity, Payment, Rating, Hour, DayOfWeek, Month]],
        columns=["Branch", "City", "Customer_Type", "Gender", "Product_Line", "Unit_Price", "Quantity", "Payment", "Rating", "Hour", "DayOfWeek", "Month"]
    )
    
    prediction = model.predict(input_data)[0]
    
    # 8. DISPLAY RESULTS
    st.markdown("---")
    st.success(f"💰 Predicted Sales: **${prediction:,.2f}**")
    
    # Provide a simple business context summary based on the prediction
    if prediction > 15000:
        st.info("📊 **Sales Status:** High-performing day expected! Check inventory levels.")
    elif prediction > 5000:
        st.info("📊 **Sales Status:** Average/Stable performance expected.")
    else:
        st.info("📊 **Sales Status:** Low sales volume projected. Consider launching a flash sale.")

    print('Sales Prediction Completed Successfully')