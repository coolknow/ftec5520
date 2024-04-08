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

def upload_record(token, doctor_id, patient_id, diagnosis):
    # files = {'image': image} if image is not None else None
    data = {'doctor_key': doctor_key, 'patient_key': patient_key, 'diagnosis': diagnosis}
    headers = {'Authorization': token}
    response = requests.post(f"{API_BASE_URL}/upload_record", data=data, headers=headers)
    if response.status_code == 200:
        st.success("Record uploaded successfully.")
    else:
        st.error("Failed to upload the record.")

def access_record(token, patient_key):
    headers = {'Authorization': token}
    response = requests.get(f"{API_BASE_URL}/access_record", params={'patient_key': patient_key}, headers=headers)
    if response.status_code == 200:
        records = response.json().get('records', [])
        return records
    else:
        st.error("Failed to access records.")
        return []

# UI
st.title("Medical Record Sharing System")

menu = ["Login", "Upload Record", "Access Record"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
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

elif choice == "Upload Record" and 'doctor_private_key' in st.session_state:
    st.subheader("Upload Patient Record")
    doctor_key = st.text_input("Doctor Key", key="doctor_id_upload")
    patient_key = st.text_input("Patient Key")
    diagnosis = st.text_area("Diagnosis")
    # image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif'])
    if st.button("Upload Record"):
        upload_record(st.session_state['doctor_private_key'], doctor_key, patient_key, diagnosis)

elif choice == "Access Record" and 'doctor_private_key' in st.session_state:
    st.subheader("Access Patient Record")
    patient_key = st.text_input("Patient key", key="patient_id_access")
    if st.button("Access Record"):
        records = access_record(st.session_state['doctor_private_key'], patient_key)
        for record in records:
            st.json(record)

else:
    st.warning("Please login to continue.")
