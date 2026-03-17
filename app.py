import streamlit as st
import requests
import datetime


with st.form(key='params_for_api'):
    date_to_predict_price = st.date_input('date a laquelle vous souhaitez prédire un prix', value=datetime.datetime(2024,1,2))
    lenght_of_prediction = st.number_input('nbre de jours pour lequelles vous voulez des prévisions horaires (0>nbre j > 2)', value=1)

    st.form_submit_button('Make prediction')

params = dict(
    date=date_to_predict_price,
    days=lenght_of_prediction)



url = 'https://power-forecast-344702926535.europe-west1.run.app/predict/from_cache'
response = requests.get(url, params=params)
