import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def edit(patient_private_key, patient_private_key_upload, patient_public_key_upload):
    data = {'patient_private_key_upload': patient_private_key_upload, 'patient_public_key_upload': patient_public_key_upload}
    headers = {'Authorization': patient_private_key}
    response = requests.post(f"{API_BASE_URL}/edit_profile", data=data, headers=headers)
    if response.status_code == 200:
        st.success("Profile edited successfully.")
    else:
        st.error("Failed to edit the profile.")

# UI
st.title("Edit Profile (Patient)")
if 'patient_private_key' in st.session_state:
    st.subheader("Edit Patient Profile")
    patient_private_key_upload = st.text_input("Patient's private key", key="patient_private_key_upload")
    patient_public_key_upload = st.text_input("Patient's public key", key="patient_public_key_upload")
    if st.button("Edit Profile"):
        edit(st.session_state['patient_private_key'], patient_private_key_upload, patient_public_key_upload)
else:
    st.warning("You must be logged in to view this page.")
