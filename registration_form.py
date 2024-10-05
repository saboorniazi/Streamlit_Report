import streamlit as st
import json
from bson import ObjectId  # Import ObjectId to handle MongoDB _id field
from pymongo import MongoClient

# MongoDB connection details (replace with your actual credentials)
MONGO_URI = "mongodb+srv://wajahat:tester1507@tester.4a1b2.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["users"]  # Select your MongoDB database
collection = db["usersdata"]   # Select the collection (table) where the form data will be stored

# Streamlit Page configuration
st.set_page_config(page_title="User Registration Form", page_icon="📝")

# Add a title
st.title("📝 User Registration Form")
st.subheader("Please fill in the details below to register")
st.markdown("---")

# Create the form
with st.form("registration_form"):
    name = st.text_input("Name *", placeholder="Enter your full name")
    email = st.text_input("Email *", placeholder="Enter your email address")
    age = st.slider("Age *", 18, 100, 25)
    message = st.text_area("Message", placeholder="Enter any additional information")
    
    agree = st.checkbox("I agree to the terms and conditions *")
    
    # Submit button
    submit_button = st.form_submit_button("Submit")

# Form validation and submission handling
if submit_button:
    if not name or not email or not agree:
        st.error("Please fill in all required fields (*) and agree to the terms.")
    else:
        # Prepare data to store in MongoDB
        user_data = {
            "name": name,
            "email": email,
            "age": age,
            "message": message
        }

        # Insert the data into MongoDB and get the inserted ID
        result = collection.insert_one(user_data)
        
        # Add the MongoDB ObjectId to user_data dictionary
        user_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        
        # Convert the data to JSON format
        user_data_json = json.dumps(user_data, indent=4)
        
        # Display success message and show JSON data
        st.success("Thank you for registering!")
        st.write("Here is your registration data in JSON format:")
        st.code(user_data_json, language="json")
