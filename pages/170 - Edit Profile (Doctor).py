import streamlit as st
import requests

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def edit(doctor_private_key, doctor_private_key_upload, doctor_public_key_upload):
    data = {'private_key': doctor_private_key_upload, 'public_key': doctor_public_key_upload}
    headers = {'Authorization': doctor_private_key}
    response = requests.post(f"{API_BASE_URL}/edit_profile", data=data, headers=headers)
    if response.status_code == 200:
        st.success("Profile edited successfully.")
    else:
        st.error("Failed to edit the profile.")

# UI
if 'doctor_private_key' in st.session_state:
    st.markdown(f"""<p style="font-size: 16px; text-align: right;">Logged in as Doctor {st.session_state['doctor_private_key']}</p>""", unsafe_allow_html=True)

st.title("Edit Profile (Doctor)")

if 'doctor_private_key' in st.session_state:
    st.subheader("Edit Doctor Profile")
    doctor_private_key_upload = st.text_input("Doctor's private key", key="doctor_private_key_upload")
    doctor_public_key_upload = st.text_input("Doctor's public key", key="doctor_public_key_upload")
    if st.button("Edit Profile"):
        edit(st.session_state['doctor_private_key'], doctor_private_key_upload, doctor_public_key_upload)
else:
    st.warning("You must be logged in to view this page.")
