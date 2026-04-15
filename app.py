import streamlit as st
import numpy as np
import pandas as pd

from auth import login
from database import init_db, save_client, get_clients
from utils import load_model

# =========================
# INIT
# =========================
init_db()
model = load_model()

st.set_page_config(page_title="Assurance SaaS PRO", layout="wide")

# =========================
# LOGIN
# =========================
if "user" not in st.session_state:
    login()
    st.stop()

st.title("🛡️ Assurance SaaS PRO")
st.sidebar.success(f"Connecté : {st.session_state['user']}")

# Déconnexion
if st.sidebar.button("Déconnexion"):
    del st.session_state["user"]
    st.rerun()

# =========================
# 👤 PROFIL CLIENT
# =========================
st.header("👤 Profil client")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Âge", 18, 80, 30)
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])

with col2:
    situation = st.selectbox("Situation", ["Célibataire", "Marié(e)", "Divorcé(e)"])
    statut = st.selectbox("Statut", ["Salarié", "Fonctionnaire", "Indépendant", "Sans emploi"])

with col3:
    anciennete = st.number_input("Ancienneté (années)", 0, 40, 2)
    compte = st.radio("Compte actif", ["Oui", "Non"])

# =========================
# 💰 REVENUS & CHARGES
# =========================
st.header("💰 Revenus & Charges")

col4, col5 = st.columns(2)

with col4:
    revenu = st.number_input("Revenu mensuel (FCFA)", 0, 10000000, 300000)
    autres_revenus = st.number_input("Autres revenus", 0, 5000000, 0)

with col5:
    charges = st.number_input("Charges mensuelles", 0, 5000000, 0)
    credit_actuel = st.number_input("Crédit en cours", 0, 5000000, 0)

revenu_total = revenu + autres_revenus
charges_total = charges + credit_actuel

taux_endettement = 0
if revenu_total > 0:
    taux_endettement = charges_total / revenu_total

st.info(f"💡 Revenu total : {revenu_total:,.0f} FCFA")
st.warning(f"⚠️ Taux d’endettement : {taux_endettement:.2%}")

# =========================
# 💳 ASSURANCE
# =========================
st.header("💳 Assurance")

col6, col7 = st.columns(2)

with col6:
    type_assurance = st.selectbox("Type", ["Auto", "Santé", "Habitation"])

with col7:
    couverture = st.number_input("Montant couverture", 0, 50000000, 5000000)

# =========================
# 🚀 ANALYSE
# =========================
if st.button("📊 Analyser le risque"):

    X = np.array([[age, revenu_total, couverture]])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    risk = round((1 - proba) * 100, 2)

    # Score couleur
    if risk < 30:
        couleur = "🟢 Bon"
        coef = 0.02
    elif risk < 60:
        couleur = "🟡 Moyen"
        coef = 0.05
    else:
        couleur = "🔴 Risqué"
        coef = 0.1

    prime = couverture * coef

    # =========================
    # 📊 RESULTATS
    # =========================
    st.subheader("💳 Score de risque")
    st.metric("Score", f"{risk} %", delta=couleur)

    st.subheader("📊 Visualisation")
    st.bar_chart({
        "Risque": [risk],
        "Fiabilité": [100 - risk]
    })

    # =========================
    # 🧠 ANALYSE IA
    # =========================
    st.subheader("🧠 Analyse IA")

    if taux_endettement > 0.4:
        st.warning("Endettement élevé")

    if revenu_total < 300000:
        st.warning("Revenu faible")

    if pred == 1:
        st.success("Profil fiable")
    else:
        st.error("Profil risqué")

    # =========================
    # 💰 PRIME
    # =========================
    st.subheader("💰 Prime Assurance")
    st.write(f"Prime estimée : {prime:,.0f} FCFA")

    # =========================
    # 💾 SAUVEGARDE
    # =========================
    save_client(age, revenu_total, couverture, risk, prime)
    st.success("Client sauvegardé ✅")

# =========================
# 📊 DASHBOARD ADMIN
# =========================
st.header("📊 Dashboard Admin")

data = get_clients()

df = pd.DataFrame(data, columns=[
    "ID","Age","Revenu","Couverture","Risque","Prime","Date"
])

st.dataframe(df)
st.bar_chart(df["Risque"])