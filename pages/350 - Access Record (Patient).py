import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def access_record(patient_private_key):
    data = {'private_key': patient_private_key}
    headers = {'Authorization': patient_private_key}
    #response = requests.get(f"{API_BASE_URL}/access_record", params={'patient_id': patient_id}, headers=headers)
    response = requests.get(f"{API_BASE_URL}/access_record", data=data, headers=headers)
    if response.status_code == 200:
        records = response.json().get('records', [])
        return records
    else:
        st.error("Failed to access records.")
        return []

# UI
if 'patient_private_key' in st.session_state:
    st.markdown(f"""<p style="font-size: 16px; text-align: right;">Logged in as Patient {st.session_state['patient_private_key']}</p>""", unsafe_allow_html=True)

st.title("Access Record (Patient)")

if 'patient_private_key' in st.session_state:
    st.subheader("Here are your medical records:")

    with st.spinner(text="Loading..."):
        # patient_id = st.text_input("Patient ID", key="patient_id_access")\
        records = access_record(st.session_state['patient_private_key'])

        noOfRecords = len(records)
        if noOfRecords == 0:
            st.markdown(f'<p style="font-size: 16px; text-align: center;">No records found.</p>', unsafe_allow_html=True)
        else:
            i = 0
            recordsList = [['' for cols in range(len(records[0]))] for rows in range(len(records))]

            for record in records:
                if record['private_key'] == st.session_state['patient_private_key']:
                    recordsList[i][0] = record['private_key']
                    recordsList[i][1] = record['diagnosis']
                    recordsList[i][2] = record['sharing']

                    # 时间戳只取年月日时分
                    recordsList[i][3] = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
                    i += 1

            recordsArray = np.array(recordsList)

            df = pd.DataFrame(data=recordsArray[:, 1:4], columns=("Diagnosis", "Sharing", "Date & Time"))
            st.dataframe(df, hide_index=True)
else:
    st.warning("You must be logged in to view this page.")
