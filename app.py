import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("carbon_model.pkl")

st.title("🌍 Carbon Footprint Tracker")

st.markdown("Fill in your details to predict your carbon emission.")

# ---------- User Input ----------
with st.form("user_input_form"):
    body_type = st.selectbox("Body Type", ["underweight", "normal", "overweight", "obese"])
    sex = st.radio("Sex", ["male", "female"])
    diet = st.selectbox("Diet", ["vegan", "vegetarian", "pescatarian", "omnivore"])
    shower = st.selectbox("How Often Shower", ["less frequently", "daily", "twice a day", "more frequently"])
    heating = st.selectbox("Heating Energy Source", ["wood", "coal", "electricity", "natural gas"])
    transport = st.selectbox("Transport", ["public", "private", "walk/bicycle"])
    vehicle_type = st.selectbox("Vehicle Type", ["petrol", "diesel", "hybrid", "electric", "lpg", ""])
    social_activity = st.selectbox("Social Activity", ["never", "sometimes", "often"])
    monthly_grocery = st.number_input("Monthly Grocery Bill", min_value=0, value=200)
    air_travel = st.selectbox("Frequency of Traveling by Air", ["never", "rarely", "frequently", "very frequently"])
    vehicle_distance = st.number_input("Vehicle Monthly Distance Km", min_value=0, value=100)
    waste_bag_size = st.selectbox("Waste Bag Size", ["small", "medium", "large", "extra large"])
    waste_bag_count = st.number_input("Waste Bag Weekly Count", min_value=0, value=1)
    tv_pc_hours = st.number_input("How Long TV/PC Daily Hour", min_value=0, value=5)
    new_clothes = st.number_input("How Many New Clothes Monthly", min_value=0, value=5)
    internet_hours = st.number_input("How Long Internet Daily Hour", min_value=0, value=5)
    energy_efficiency = st.selectbox("Energy Efficiency", ["Yes", "No", "Sometimes"])
    recycling = st.multiselect("Recycling", ["Paper", "Plastic", "Glass", "Metal"])
    cooking_with = st.multiselect("Cooking With", ["Stove", "Oven", "Microwave", "Grill", "Airfryer"])

    submit_button = st.form_submit_button(label="Predict Carbon Emission")

# ---------- Prediction ----------
if submit_button:
    # Prepare input data
    input_dict = {
        "Body Type": [body_type],
        "Sex": [sex],
        "Diet": [diet],
        "How Often Shower": [shower],
        "Heating Energy Source": [heating],
        "Transport": [transport],
        "Vehicle Type": [vehicle_type],
        "Social Activity": [social_activity],
        "Monthly Grocery Bill": [monthly_grocery],
        "Frequency of Traveling by Air": [air_travel],
        "Vehicle Monthly Distance Km": [vehicle_distance],
        "Waste Bag Size": [waste_bag_size],
        "Waste Bag Weekly Count": [waste_bag_count],
        "How Long TV PC Daily Hour": [tv_pc_hours],
        "How Many New Clothes Monthly": [new_clothes],
        "How Long Internet Daily Hour": [internet_hours],
        "Energy efficiency": [energy_efficiency],
        "Recycling": [recycling],
        "Cooking_With": [cooking_with]
    }

    input_df = pd.DataFrame(input_dict)

    # OPTIONAL: apply same preprocessing used during training (encoding, scaling, etc.)
    # For now assuming your model accepts raw inputs like this
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Estimated Carbon Emission: **{prediction} kg CO₂**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
