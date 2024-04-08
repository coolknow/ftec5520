import streamlit as st
import pandas as pd
import requests
import json

# Assuming your Flask API is running on localhost:5000
API_BASE_URL = "http://localhost:5000"

def access_record(patient_private_key, patient_id):
    headers = {'Authorization': patient_private_key}
    response = requests.get(f"{API_BASE_URL}/access_record", params={'patient_id': patient_id}, headers=headers)
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
    st.subheader("Access Patient Record")

    patient_id = st.text_input("Patient ID", key="patient_id_access")
    if st.button("Access Record"):
        records = access_record(st.session_state['patient_private_key'], patient_id)

        noOfRecords = len(records)
        if noOfRecords == 0:
            st.markdown(f'<p style="font-size: 16px; text-align: center;">No records found.</p>', unsafe_allow_html=True)
        else:
            i = 0
            recordsArray = [['' for cols in range(len(records[0]))] for rows in range(len(records))]

            for record in records:
                recordsArray[i][0] = str(record['id'])
                recordsArray[i][1] = record['record']
                i += 1

            df = pd.DataFrame(data=recordsArray, columns=("ID", "Record"))
            st.dataframe(df, hide_index=True)
            # st.markdown("<table><tr><th>ID</th><th>Record</th>")
            #
            # for record in records:
            #     st.markdown("<tr><td>")
            #     st.write(record)
            #     st.markdown("<td>2024-04-08</td></tr>")
            #
            #     #st.json(record)
            #
            # st.markdown("</table>")

else:
    st.warning("You must be logged in to view this page.")
