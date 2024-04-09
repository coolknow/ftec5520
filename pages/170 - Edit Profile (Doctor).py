import streamlit as st
import requests
import csv
from datetime import datetime
import numpy as np

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def get_latest_record(doctor_private_key):
    filename = 'basic_information.csv'
    latest_record = []
    found_records = False

    with open(filename, 'r', encoding='UTF-8', newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',', quotechar='\"')
        rowCount = 0

        for row in csvReader:
            rowCount += 1

            if rowCount == 1:
                latest_record = ['' for cols in range(len(row))]
                continue

            if len(row) == 0:
                continue

            # check if the current row is a doctor and if the private key matches the session stored private key
            if row[0] == 'Doctor' and row[1] == doctor_private_key:
                if not found_records:
                    latest_record = row
                    found_records = True
                else:
                    # check the timestamp as well
                    if datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(latest_record[4], '%Y-%m-%d %H:%M:%S.%f'):
                        latest_record = row

    csvFile.close()
    
    return latest_record

def edit(doctor_private_key, doctor_private_key_upload, doctor_public_key_upload, doctor_name_upload):
    data = {'role': 'Doctor', 'private_key': doctor_private_key_upload, 'public_key': doctor_public_key_upload, 'name': doctor_name_upload}
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

    # Load in Doctor's existing profile, if one exists
    row = get_latest_record(st.session_state['doctor_private_key'])

    doctor_private_key_upload = st.text_input("Doctor's private key", value=row[1], key="doctor_private_key_upload")
    doctor_public_key_upload = st.text_input("Doctor's public key", value=row[2], key="doctor_public_key_upload")
    doctor_name_upload = st.text_input("Doctor's name", value=row[3], key="doctor_name_upload")

    if st.button("Edit Profile"):
        edit(st.session_state['doctor_private_key'], doctor_private_key_upload, doctor_public_key_upload, doctor_name_upload)
else:
    st.warning("You must be logged in to view this page.")
