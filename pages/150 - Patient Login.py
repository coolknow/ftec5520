import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def login(role = 'Patient', patient_id, password):
    response = requests.post(f"{API_BASE_URL}/login", data={'role': role, 'patient_id': patient_id, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        st.error("Failed to log in. Please check your credentials.")
        return None

# UI
st.title("Login")

st.subheader("Patient Login")
patient_id = st.text_input("Patient ID")
password = st.text_input("Password", type='password')
if st.button("Login"):
    token = login(patient_id, password)
    st.session_state['token'] = token
