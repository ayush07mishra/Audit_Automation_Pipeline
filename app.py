import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="AI Audit System", layout="wide")

st.title("💼 AI-Powered Audit Automation System")

# Load pipeline (IMPORTANT: not just model)
pipeline = joblib.load("model/isolation_pipeline.pkl")

file = st.file_uploader("Upload Transaction CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # --- Data Cleaning ---
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])

    # --- Feature Engineering (SAME AS TRAINING) ---
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday

    df['customer_freq'] = df['customer_id'].map(df['customer_id'].value_counts())
    df['type'] = df['type'].map({'credit': 1, 'debit': 0})
    df['desc_length'] = df['description'].apply(len)

    features = [
        'amount', 'type', 'year', 'month', 'day',
        'weekday', 'customer_freq', 'desc_length'
    ]

    X = df[features]

    # --- Predict ---
    df['anomaly'] = pipeline.predict(X)
    df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

    # score (access model inside pipeline)
    df['score'] = pipeline.named_steps['model'].decision_function(
        pipeline.named_steps['scaler'].transform(X)
    )

    # --- Rules ---
    df['high_amount'] = df['amount'] > df['amount'].mean() * 2
    df['weekend'] = df['weekday'] >= 5
    df['low_freq_customer'] = df['customer_freq'] < 3

    df['final_flag'] = (
        (df['anomaly'] == 1) |
        df['high_amount'] |
        df['weekend'] |
        df['low_freq_customer']
    )

    # --- Explanation ---
    def explain(row):
        reasons = []
        if row['high_amount']:
            reasons.append("High amount")
        if row['weekend']:
            reasons.append("Weekend")
        if row['low_freq_customer']:
            reasons.append("Rare customer")
        if row['anomaly'] == 1:
            reasons.append("ML anomaly")
        return ", ".join(reasons)

    df['reason'] = df.apply(explain, axis=1)

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Suspicious", df['final_flag'].sum())
    col3.metric("Rate (%)", round(df['final_flag'].mean()*100, 2))

    st.divider()

    # --- Fraud Gauge ---
    st.subheader("⚡ Fraud Risk Score")

    avg_score = np.mean(df['score'])

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_score,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [-0.5, 0.5]},
            'steps': [
                {'range': [-0.5, -0.1], 'color': "green"},
                {'range': [-0.1, 0.1], 'color': "yellow"},
                {'range': [0.1, 0.5], 'color': "red"}
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # --- Alerts ---
    st.subheader("🚨 Live Alerts")

    alerts = df[df['final_flag'] == True]

    if not alerts.empty:
        for _, row in alerts.head(5).iterrows():
            st.error(f"Tx {row['transaction_id']} → {row['reason']}")
    else:
        st.success("No suspicious activity")

    st.divider()

    # --- Filters ---
    st.sidebar.header("Filters")

    min_amount = st.sidebar.slider("Min Amount", 0, int(df['amount'].max()), 0)
    show_flagged = st.sidebar.checkbox("Only Suspicious")

    filtered = df[df['amount'] >= min_amount]

    if show_flagged:
        filtered = filtered[filtered['final_flag'] == True]

    # --- Tables ---
    st.subheader("📋 Transactions")
    st.dataframe(filtered, use_container_width=True)

    st.subheader("🚨 Suspicious")
    st.dataframe(df[df['final_flag']], use_container_width=True)

    # --- Charts ---
    st.subheader("📊 Analytics")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.hist(df['amount'], bins=40)
        ax.set_title("Amount Distribution")
        st.pyplot(fig)

    with col2:
        counts = df['final_flag'].value_counts()
        fig2, ax2 = plt.subplots()
        counts.plot(kind='bar', ax=ax2)
        ax2.set_title("Normal vs Suspicious")
        st.pyplot(fig2)

    # --- Drilldown ---
    st.subheader("🔎 Transaction Details")

    selected = st.selectbox("Transaction ID", df['transaction_id'])
    st.write(df[df['transaction_id'] == selected])

    # --- Download ---
    st.download_button(
        "Download Results",
        df.to_csv(index=False),
        file_name="audit_results.csv"
    )

else:
    st.info("Upload a CSV file")