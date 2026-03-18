import streamlit as st
import requests
import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Prédictions de prix",
    page_icon="📈",
    layout="wide",
)


with st.form(key='params_for_api'):
    date_to_predict_price = st.date_input('date a laquelle vous souhaitez prédire un prix', value=datetime.datetime(2024,3,20))
    lenght_of_prediction = st.number_input('nombre de jours pour lesquelles vous voulez des prévisions horaires', value=2)

    if st.form_submit_button('Make prediction'):

        params = dict(
            date=date_to_predict_price,
            days=lenght_of_prediction)

        url = 'https://power-forecast-344702926535.europe-west1.run.app/predict/combined'
        response = requests.get(url, params=params)

        result = response.json()

        pred = result['predictions']

        dates = [p['date'] for p in pred]
        rnn = [p['prix_predit_rnn'] for p in pred]
        xgb = [p['prix_predit_xgb'] for p in pred]
        reel = [p['prix_reel'] for p in pred]

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=dates, y=reel, mode='lines', name='Prix réel', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=dates, y=rnn, mode='lines', name='LSTM', line=dict(color='blue', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=dates, y=xgb, mode='lines', name='XGBoost', line=dict(color='orange', width=3, dash='dash')))

        fig.update_layout(title='Prédictions de prix vs Prix réel', yaxis_title='Prix (EUR/MWh)', height=500)

        st.plotly_chart(fig, use_container_width=True)
