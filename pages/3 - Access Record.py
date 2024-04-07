import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def access_record(token, patient_id):
    headers = {'Authorization': token}
    response = requests.get(f"{API_BASE_URL}/access_record", params={'patient_id': patient_id}, headers=headers)
    if response.status_code == 200:
        records = response.json().get('records', [])
        return records
    else:
        st.error("Failed to access records.")
        return []

# UI
st.title("Access Record")

if 'token' in st.session_state:
    st.subheader("Access Patient Record")
    patient_id = st.text_input("Patient ID", key="patient_id_access")
    if st.button("Access Record"):
        records = access_record(st.session_state['token'], patient_id)
        for record in records:
            st.json(record)
else:
    st.warning("Please login to continue.")