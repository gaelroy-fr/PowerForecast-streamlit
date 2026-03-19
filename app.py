import streamlit as st
import requests
import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Prédictions de prix",
    page_icon="📈",
    layout="wide",
)

# ── Header ────────────────────────────────────────────────────
col_title, col_logo = st.columns([5, 1])

with col_title:
    st.title("⚡ Power Forecast")
    st.subheader("Prédiction horaire des prix de l'électricité - Day-Ahead (EUR/MWh)")

with col_logo:
    st.image("https://www.logotheque-vectorielle.fr/wp-content/uploads/2022/10/logo-vectoriel-le-wagon.jpg", width=850)

st.divider()


# ── Main layout: sidebar controls | chart ─────────────────────
col_controls, col_chart = st.columns([1, 3])

with col_controls:
    st.markdown("### 📅 Paramètres")
    st.caption("Sélectionnez une date et un nombre de jours.")

    with st.form(key='params_for_api'):
        date_to_predict_price = st.date_input(
            '📆 Date de départ',
            value=datetime.datetime(2024, 3, 1)
        )
        lenght_of_prediction = st.number_input(
            '📊 Jours à prédire',
            value=2, min_value=1, max_value=14
        )
        st.write("")
        submitted = st.form_submit_button('▶ Lancer', use_container_width=True)

with col_chart:
    if submitted:
        params = dict(date=date_to_predict_price, days=lenght_of_prediction)

        url = 'https://power-forecast-344702926535.europe-west1.run.app/predict/combined'

        with st.spinner("Chargement des prédictions…"):
            response = requests.get(url, params=params)
            result = response.json()

        pred  = result['predictions']
        dates = [p['date'] for p in pred]
        rnn   = [p['prix_predit_rnn'] for p in pred]
        xgb   = [p['prix_predit_xgb'] for p in pred]
        reel  = [p['prix_reel'] for p in pred]


        mae_lstm = 12.03
        mae_xgb  = 10.97

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=reel, mode='lines', name='Prix réel',
                                 line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=dates, y=rnn, mode='lines', name=f'LSTM',
                                 line=dict(color='blue', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=dates, y=xgb, mode='lines', name=f'XGBoost ',
                                 line=dict(color='red', width=3, dash='dash')))

        fig.add_annotation(
            text=f"<b>MAE LSTM : {mae_lstm} €/MWh<br>MAE XGBoost : {mae_xgb} €/MWh</b>",
            xref="paper", yref="paper",
            x=0.01, y=0.97,
            showarrow=False,
            align="left",
            bgcolor="rgba(0,0,0,0.55)",
            bordercolor="rgba(255,255,255,0.15)",
            borderwidth=1,
            borderpad=8,
            font=dict(color="white", size=13),
        )

        fig.update_layout(
            title='Prédictions de prix vs Prix réel',
            yaxis_title='Prix (EUR/MWh)',
            height=470,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=15),
            )
        )


        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("👈 Renseigne les paramètres et lance la prédiction.")