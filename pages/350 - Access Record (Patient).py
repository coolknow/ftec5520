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

def onChangeSharing(patient_private_key, diagnosis, sharing, full_diagnosis_date):
    data = {'private_key': patient_private_key, 'diagnosis': diagnosis, 'sharing': sharing, 'full_diagnosis_date': full_diagnosis_date}
    headers = {'Authorization': patient_private_key}
    response = requests.post(f"{API_BASE_URL}/update_sharing", data=data, headers=headers)

    if response.status_code == 200:
        st.success("Record sharing status updated successfully.")
    else:
        st.error("Failed to update the record sharing status.")

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
            recordsList = [['' for cols in range(6)] for rows in range(len(records))]
            diagnosisDatesList = []

            # Find all "diagnosis_date"s for this patient (duplicates removed)
            for record in records:
                if record['private_key'] == st.session_state['patient_private_key']:
                    diagnosisDatesList.append(record['diagnosis_date'])
                    diagnosisDatesList = list(dict.fromkeys(diagnosisDatesList)) # remove duplicates

            diagnosisLastUpdateDates = dict.fromkeys(diagnosisDatesList) # key: diagnosis_date, value: latest last_update_date

            i = 0
            for record in records:
                #if record['private_key'] == st.session_state['patient_private_key']:

                if (diagnosisLastUpdateDates[record['diagnosis_date']] is None) or (record['last_update_date'] > diagnosisLastUpdateDates[record['diagnosis_date']]['lastUpdateDate']):
                    diagnosisLastUpdateDates[record['diagnosis_date']] = {'index': i, 'lastUpdateDate': record['last_update_date']}

                    recordsList[i][0] = record['private_key']

                    # 时间戳只取年月日时分
                    recordsList[i][1] = datetime.strptime(record['diagnosis_date'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')

                    recordsList[i][2] = record['diagnosis']
                    recordsList[i][3] = (record['sharing'] == "Public") # True only if Sharing is set to Public
                    recordsList[i][4] = record['diagnosis_date']
                    recordsList[i][5] = record['last_update_date']

                    i += 1

            # Display only the latest medical record for each diagnosis.  These are the entries at the indices "diagnosisLastUpdateDates[record['diagnosis_date']]['index'] for each 'diagnosis_date'
            indicesToShow = []
            for diagnosisLastUpdateDate in diagnosisLastUpdateDates:
                indicesToShow.append(diagnosisLastUpdateDates[diagnosisLastUpdateDate]['index'])

            recordsArray = np.array(recordsList)

            df = pd.DataFrame(data=recordsArray[indicesToShow], columns=("Private Key", "Diagnosis Date", "Diagnosis", "Sharing", "Full Diagnosis Date", "Last Update Date"))

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
                    ),
                    "Private Key": None, #None means hide it in the table
                    "Full Diagnosis Date": None,
                    "Last Update Date": None
                },
            )

            if edited_df is not None and not edited_df.equals(st.session_state["df_value"]):
                df_to_dict = df.to_dict()
                edited_df_to_dict = edited_df.to_dict()

                id_of_changed_sharing = -1 # id within df_to_dict['Sharing'] of the entry whose sharing was changed

                for id in df_to_dict['Sharing']:
                    if df_to_dict['Sharing'][id] != edited_df_to_dict['Sharing'][id]:
                        id_of_changed_sharing = id
                        break

                onChangeSharing(
                    st.session_state['patient_private_key'],
                    edited_df_to_dict['Diagnosis'][id],
                    edited_df_to_dict['Sharing'][id],
                    edited_df_to_dict['Full Diagnosis Date'][id]
                )

                st.session_state["df_value"] = edited_df
else:
    st.warning("You must be logged in to view this page.")
