import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load trained model
model = joblib.load("carbon_model.pkl")

# Page layout
st.set_page_config(page_title="Carbon Footprint Tracker", layout="wide")
st.title("🌱 Carbon Footprint Tracker")
st.markdown("Estimate your monthly carbon footprint based on lifestyle and habits.")

# -----------------------------
# Collapsible input sections
# -----------------------------
with st.expander("Personal Info"):
    body_type = st.selectbox("Body Type", ["underweight","normal","overweight","obese"])
    sex = st.selectbox("Sex", ["male","female"])
    diet = st.selectbox("Diet", ["vegetarian","vegan","pescatarian","omnivore"])
    shower = st.selectbox("How Often Shower", ["less frequently","more frequently","twice a day","daily"])

with st.expander("Home & Energy"):
    heating = st.selectbox("Heating Energy Source", ["coal","wood","natural gas","electricity","lpg"])
    energy_efficiency = st.radio("Energy Efficiency", ["Yes","No","Sometimes"])
    cooking_with = st.multiselect("Cooking With", ["Stove","Oven","Microwave","Grill","Airfryer"])

with st.expander("Transport & Vehicle"):
    transport = st.selectbox("Transport", ["walk/bicycle","public","private"])
    vehicle_type = st.selectbox("Vehicle Type", ["petrol","diesel","electric","hybrid",""])
    vehicle_km = st.number_input("Vehicle Monthly Distance (Km)", min_value=0.0, value=0.0)
    air_travel_freq = st.selectbox("Frequency of Traveling by Air", ["never","rarely","frequently","very frequently"])
    
with st.expander("Lifestyle & Consumption"):
    social_activity = st.selectbox("Social Activity", ["never","sometimes","often"])
    monthly_grocery = st.number_input("Monthly Grocery Bill ($)", min_value=0.0, value=100.0)
    waste_size = st.selectbox("Waste Bag Size", ["small","medium","large","extra large"])
    waste_count = st.number_input("Waste Bag Weekly Count", min_value=0, value=1)
    tv_pc_hours = st.number_input("TV/PC Daily Hour", min_value=0, value=2)
    new_clothes = st.number_input("How Many New Clothes Monthly", min_value=0, value=2)
    internet_hours = st.number_input("How Long Internet Daily Hour", min_value=0, value=3)
    recycling = st.multiselect("Recycling", ["Paper","Plastic","Glass","Metal"])

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Carbon Footprint"):
    input_df = pd.DataFrame([[
        body_type, sex, diet, shower, heating, transport, vehicle_type, social_activity,
        monthly_grocery, air_travel_freq, vehicle_km, waste_size, waste_count, tv_pc_hours,
        new_clothes, internet_hours, energy_efficiency, recycling, cooking_with
    ]], columns=[
        "Body Type","Sex","Diet","How Often Shower","Heating Energy Source","Transport",
        "Vehicle Type","Social Activity","Monthly Grocery Bill","Frequency of Traveling by Air",
        "Vehicle Monthly Distance Km","Waste Bag Size","Waste Bag Weekly Count",
        "How Long TV PC Daily Hour","How Many New Clothes Monthly","How Long Internet Daily Hour",
        "Energy efficiency","Recycling","Cooking_With"
    ])
    
    prediction = model.predict(input_df)[0]
    st.success(f"✅ Estimated Carbon Emission: {prediction:.2f} kg CO2/month")

    # -----------------------------
    # Visualize top contributors (numeric)
    # -----------------------------
    factors = {
        "Monthly Grocery": monthly_grocery,
        "Vehicle Distance Km": vehicle_km,
        "TV/PC Hours": tv_pc_hours,
        "New Clothes": new_clothes,
        "Internet Hours": internet_hours,
        "Waste Count": waste_count
    }
    chart_df = pd.DataFrame(list(factors.items()), columns=["Category","Value"]).sort_values(by="Value", ascending=False)
    fig = px.bar(chart_df, x="Category", y="Value", text="Value", color="Value", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Tips
    # -----------------------------
    st.markdown("### Tips to Reduce Carbon Footprint")
    st.markdown("""
    - Use energy-efficient heating and appliances  
    - Reduce car and air travel; use public transport, walking, or cycling  
    - Eat more plant-based meals  
    - Minimize waste and recycle effectively  
    - Reduce screen time and unnecessary consumption
    """)
