import streamlit as st
import requests
import datetime


with st.form(key='params_for_api'):
    date_to_predict_price = st.date_input('date a laquelle vous souhaitez prédire un prix', value=datetime.datetime(2024,1,2))

    st.form_submit_button('Make prediction')

params = dict(
    date_to_predict_price=date_to_predict_price)

url = 'https://powerforecast-344702926535.europe-west1.run.app/predict/from_cache'
response = requests.get(url, params=params)
