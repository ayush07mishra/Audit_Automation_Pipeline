# 💼 AI-Powered Audit Automation System

An interactive machine learning project that detects suspicious financial transactions using anomaly detection + rule-based auditing, and presents results through a Streamlit dashboard.

---

# 🚀 Project Overview

This system analyzes transaction data and automatically flags unusual or risky activities using:

* 🤖 Machine Learning (Isolation Forest)
* 📊 Statistical rules (audit logic)
* 📈 Interactive dashboard (Streamlit)

It is designed to simulate a real-world audit pipeline used in finance and fraud detection.

---

# 🧠 How It Works

The system combines **two approaches**:

### 1. Machine Learning Detection

* Learns normal transaction patterns
* Flags deviations (anomalies)

### 2. Rule-Based Auditing

* High transaction amount
* Weekend activity
* Low-frequency customers

### Final Decision:

A transaction is marked **suspicious if ANY condition is true**

---

# 📁 Project Structure

```
audit_project/
│── data/
│   └── transactions.csv
│
│── notebooks/
│   └── audit_model.ipynb
│
│── models/
│   └── isolation_pipeline.pkl
│
│── app.py
│── requirements.txt
│── README.md
```

---

# ⚙️ Installation

```bash
git clone <https://github.com/ayush07mishra/Audit_Automation_Pipeline>
cd audit_project

pip install -r requirements.txt
```

---

# 📦 Requirements

```
pandas
numpy
scikit-learn
streamlit
joblib
matplotlib
plotly
```

---

# 📊 Dataset Format

Your dataset must contain:

| Column         | Description         |
| -------------- | ------------------- |
| transaction_id | Unique ID           |
| date           | Transaction date    |
| customer_id    | Customer identifier |
| amount         | Transaction amount  |
| type           | credit / debit      |
| description    | Transaction notes   |

---

# 🧪 Model Training (Notebook)

Run:

```
notebooks/audit_model.ipynb
```

### What happens:

* Feature engineering
* Model training using Isolation Forest
* Pipeline creation (scaler + model)
* Saved as:

```
models/isolation_pipeline.pkl
```

---

# ▶️ Run Streamlit App

```bash
streamlit run app.py
```

---

# 🖥️ Features in UI

### 📊 Dashboard Metrics

* Total transactions
* Suspicious transactions
* Anomaly rate

---

### ⚡ Fraud Risk Gauge

* Shows overall system risk level
* Based on anomaly scores

---

### 🚨 Live Alerts

* Displays top suspicious transactions
* Shows reason for each flag

---

### 🔍 Filters

* Minimum transaction amount
* Show only suspicious data

---

### 📋 Data Tables

* Full dataset view
* Suspicious transactions only

---

### 📊 Visualizations

* Amount distribution histogram
* Normal vs suspicious comparison

---

### 🔎 Drill-down Analysis

* Select any transaction
* View full details

---

### ⬇️ Export Results

* Download processed CSV with flags

---

# 🧠 Feature Engineering

The model uses:

```
amount
type (encoded)
year
month
day
weekday
customer_freq
desc_length
```

---

# 🚨 Suspicious Detection Logic

A transaction is flagged if:

* ML model detects anomaly
  OR
* Amount is unusually high
  OR
* Occurs on weekend
  OR
* Customer appears rarely

---

# 📌 Example Output

| transaction_id | amount | reason                  |
| -------------- | ------ | ----------------------- |
| 102            | 9000   | High amount, ML anomaly |
| 245            | 500    | Weekend, Rare customer  |

---

# ⚠️ Important Notes

* Training and prediction features must match exactly
* Always retrain model after changing features
* Use pipeline to avoid feature mismatch errors

---

# 🔧 Common Errors & Fixes

### ❌ Feature mismatch error

✔ Retrain model and reload correct `.pkl`

### ❌ Wrong model loaded

✔ Ensure using:

```
isolation_pipeline.pkl
```

---

# 🚀 Future Improvements

* Real-time transaction streaming
* Email / SMS alerts
* Fraud probability scoring
* SHAP explainability
* Cloud deployment

---

# 📌 Summary

This project demonstrates:

* End-to-end ML pipeline
* Real-world audit logic
* Interactive analytics dashboard
* Explainable anomaly detection

---

# 👨‍💻 Author

Ayush Mishra

---

# ⭐ If you found this useful

Give it a star and improve it further 🚀
