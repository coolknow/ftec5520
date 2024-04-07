import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def upload_record(token, doctor_id, patient_id, diagnosis, image):
    files = {'image': image} if image is not None else None
    data = {'doctor_id': doctor_id, 'patient_id': patient_id, 'diagnosis': diagnosis}
    headers = {'Authorization': token}
    response = requests.post(f"{API_BASE_URL}/upload_record", files=files, data=data, headers=headers)
    if response.status_code == 200:
        st.success("Record uploaded successfully.")
    else:
        st.error("Failed to upload the record.")

# UI
st.title("Upload Record")
if 'token' in st.session_state:
    st.subheader("Upload Patient Record")
    doctor_id = st.text_input("Doctor ID", key="doctor_id_upload")
    patient_id = st.text_input("Patient ID")
    diagnosis = st.text_area("Diagnosis")
    image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif'])
    if st.button("Upload Record"):
        upload_record(st.session_state['token'], doctor_id, patient_id, diagnosis, image)
else:
    st.warning("Please login to continue.")
