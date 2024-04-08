import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def login(patient_private_key):
    response = requests.post(f"{API_BASE_URL}/login", data={'patient_private_key':patient_private_key})
    if response.status_code == 200:
        return patient_private_key
    else:
        st.error("Failed to log in. Please check your credentials.")
        return None

# UI
st.title("Login")

if 'patient_private_key' not in st.session_state:
    st.subheader("Patient Login")
    patient_private_key = st.text_input("Patient ID")
    if st.button("Login"):
        token = login(patient_private_key)
        st.session_state['patient_private_key'] = patient_private_key
        st.rerun()
else:
    patient_private_key = st.session_state['patient_private_key']
    st.write(f'Welcome {patient_private_key}')
