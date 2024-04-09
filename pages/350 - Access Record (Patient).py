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

def onChangeSharing(edited_df):
    print("Do stuff")

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
                    recordsList[i][2] = record['diagnosis']
                    recordsList[i][3] = (record['sharing'] == "Public") # True only if Sharing is set to Public

                    # 时间戳只取年月日时分
                    recordsList[i][1] = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
                    i += 1

            recordsArray = np.array(recordsList)
            print(recordsArray)

            df = pd.DataFrame(data=recordsArray[:, 1:4], columns=("Date & Time", "Diagnosis", "Sharing"))

            if "df_value" not in st.session_state:
                st.session_state.df_value = df

            edited_df = st.data_editor(
                df,
                #key=f"editor",
                hide_index=True,
                column_config={
                    "Sharing": st.column_config.CheckboxColumn(
                        help="Check the boxes next to the medical records if you wish to allow doctors to view them.",
                        label="Sharing"
                    )
                },
            )

            if edited_df is not None and not edited_df.equals(st.session_state["df_value"]):
                # This will only run if
                # 1. Some widget has been changed (including the dataframe editor), triggering a
                # script rerun, and
                # 2. The new dataframe value is different from the old value
                onChangeSharing(edited_df)
                st.session_state["df_value"] = edited_df


else:
    st.warning("You must be logged in to view this page.")
