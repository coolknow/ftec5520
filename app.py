import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def login(doctor_id, password):
    response = requests.post(f"{API_BASE_URL}/login", data={'doctor_id': doctor_id, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        st.error("Failed to log in. Please check your credentials.")
        return None

def upload_record(token, doctor_id, patient_id, diagnosis, image):
    files = {'image': image} if image is not None else None
    data = {'doctor_id': doctor_id, 'patient_id': patient_id, 'diagnosis': diagnosis}
    headers = {'Authorization': token}
    response = requests.post(f"{API_BASE_URL}/upload_record", files=files, data=data, headers=headers)
    if response.status_code == 200:
        st.success("Record uploaded successfully.")
    else:
        st.error("Failed to upload the record.")

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
st.title("Medical Record Sharing System")

#menu = ["Login", "Upload Record", "Access Record"]
#choice = st.sidebar.selectbox("Menu", menu)
c = st.container()
c.write("Hi")

#
# if choice == "Login":
#     st.subheader("Doctor Login")
#     doctor_id = st.text_input("Doctor ID")
#     password = st.text_input("Password", type='password')
#     if st.button("Login"):
#         token = login(doctor_id, password)
#         st.session_state['token'] = token
#
# elif choice == "Upload Record" and 'token' in st.session_state:
#     st.subheader("Upload Patient Record")
#     doctor_id = st.text_input("Doctor ID", key="doctor_id_upload")
#     patient_id = st.text_input("Patient ID")
#     diagnosis = st.text_area("Diagnosis")
#     image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'gif'])
#     if st.button("Upload Record"):
#         upload_record(st.session_state['token'], doctor_id, patient_id, diagnosis, image)
#
# elif choice == "Access Record" and 'token' in st.session_state:
#     st.subheader("Access Patient Record")
#     patient_id = st.text_input("Patient ID", key="patient_id_access")
#     if st.button("Access Record"):
#         records = access_record(st.session_state['token'], patient_id)
#         for record in records:
#             st.json(record)
#
# else:
#     st.warning("Please login to continue.")
