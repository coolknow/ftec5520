import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def login(doctor_private_key):
    response = requests.post(f"{API_BASE_URL}/login", data={'doctor_private_key':doctor_private_key})
    if response.status_code == 200:
        return doctor_private_key
    else:
        st.error("Failed to log in. Please check your credentials.")
        return None

# UI
st.title("Login")

if 'doctor_private_key' not in st.session_state:
    st.subheader("Doctor Login")
    doctor_private_key = st.text_input("Doctor ID")
    if st.button("Login"):
        token = login(doctor_private_key)
        st.session_state['doctor_private_key'] = doctor_private_key
        st.rerun()
else:
    doctor_private_key = st.session_state['doctor_private_key']
    st.write(f'Welcome {doctor_private_key}')
