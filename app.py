import streamlit as st
import numpy as np
import pandas as pd

from auth import login
from database import init_db, save_client, get_clients
from utils import load_model

# INIT
init_db()
model = load_model()

st.set_page_config(page_title="Assurance SaaS", layout="wide")

# LOGIN
if "user" not in st.session_state:
    login()
    st.stop()

st.title("🛡️ Assurance SaaS Platform")

st.sidebar.success(f"Connecté: {st.session_state['user']}")

# =========================
# 👤 CLIENT
# =========================
st.header("👤 Nouveau client")

age = st.slider("Âge", 18, 80, 30)
revenu = st.number_input("Revenu mensuel", 0, 10000000, 300000)
couverture = st.number_input("Couverture", 0, 50000000, 5000000)

# =========================
# 🚀 ANALYSE
# =========================
if st.button("Analyser"):

    X = np.array([[age, revenu, couverture]])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    risk = round((1 - proba) * 100, 2)

    if risk < 30:
        coefficient = 0.02
    elif risk < 60:
        coefficient = 0.05
    else:
        coefficient = 0.1

    prime = couverture * coefficient

    st.metric("Risque", f"{risk} %")
    st.write("💰 Prime:", prime)

    save_client(age, revenu, couverture, risk, prime)

    st.success("Client sauvegardé ✅")

# =========================
# 📊 ADMIN DASHBOARD
# =========================
st.header("📊 Dashboard Admin")

data = get_clients()

df = pd.DataFrame(data, columns=[
    "ID","Age","Revenu","Couverture","Risque","Prime","Date"
])

st.dataframe(df)
st.bar_chart(df["Risque"])