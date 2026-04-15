import streamlit as st
import numpy as np
import pandas as pd
import io
from datetime import datetime
from fpdf import FPDF

from auth import auth_page
from database import init_users, save_client, get_clients
from utils import load_model

# =========================
# INIT
# =========================
init_users()
model = load_model()

st.set_page_config(page_title="Assurance SaaS PRO", layout="wide")

# =========================
# AUTH
# =========================
if "user" not in st.session_state:
    auth_page()
    st.stop()

st.title("🛡️ Assurance SaaS - Version PRO 2.0")
st.caption("Système intelligent d’évaluation de risque assurance")

st.sidebar.success(f"Connecté : {st.session_state['user']}")

if st.sidebar.button("🔓 Déconnexion"):
    del st.session_state["user"]
    st.rerun()

# =========================
# 👤 PROFIL CLIENT
# =========================
st.header("👤 Profil assuré")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Âge", 18, 80, 30)
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])

with col2:
    situation = st.selectbox("Situation matrimoniale", ["Célibataire", "Marié(e)", "Divorcé(e)"])
    statut = st.selectbox("Statut professionnel", ["Salarié", "Fonctionnaire", "Indépendant", "Sans emploi"])

with col3:
    anciennete = st.number_input("Ancienneté (années)", 0, 40, 2)
    compte_actif = st.radio("Compte bancaire actif", ["Oui", "Non"])

# =========================
# 💰 FINANCES
# =========================
st.header("💰 Revenus & Charges")

col4, col5 = st.columns(2)

with col4:
    revenu = st.number_input("Revenu mensuel (FCFA)", 0, 10000000, 300000)
    autres_revenus = st.number_input("Autres revenus (FCFA)", 0, 5000000, 0)

with col5:
    credit_actuel = st.number_input("Mensualité crédit actuel (FCFA)", 0, 5000000, 0)
    autres_charges = st.number_input("Autres charges (FCFA)", 0, 5000000, 0)

revenu_total = revenu + autres_revenus
charges_total = credit_actuel + autres_charges

taux_endettement = charges_total / revenu_total if revenu_total > 0 else 0

st.info(f"💡 Revenu total : {revenu_total:,.0f} FCFA")
st.warning(f"⚠️ Taux d’endettement : {taux_endettement:.2%}")

# =========================
# 💳 CONTRAT
# =========================
st.header("💳 Contrat d’assurance")

col6, col7 = st.columns(2)

with col6:
    type_assurance = st.selectbox("Type d'assurance", ["Auto", "Santé", "Habitation"])

with col7:
    couverture = st.number_input("Montant couverture (FCFA)", 0, 50000000, 5000000)

# =========================
# 🚀 ANALYSE
# =========================
if st.button("📊 Analyser le risque assurance"):

    X = np.array([[age, revenu_total, couverture]])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    risk = round((1 - proba) * 100, 2)

    # SCORE
    if risk < 30:
        statut_risk = "🟢 Faible risque"
        coef = 0.02
    elif risk < 60:
        statut_risk = "🟡 Risque moyen"
        coef = 0.05
    else:
        statut_risk = "🔴 Risque élevé"
        coef = 0.10

    prime = couverture * coef

    # =========================
    # AFFICHAGE
    # =========================
    st.subheader("💳 Score de risque")
    st.metric("Score assurance", f"{risk} %", delta=statut_risk)

    st.subheader("📊 Visualisation")
    st.bar_chart({
        "Risque": [risk],
        "Fiabilité": [100 - risk]
    })

    st.subheader("🧠 Analyse intelligente")

    if taux_endettement > 0.4:
        st.warning("⚠️ Endettement élevé")

    if revenu_total < 300000:
        st.warning("⚠️ Revenu faible")

    if pred == 1:
        st.success("✔ Profil acceptable")
    else:
        st.error("❌ Profil à risque")

    st.subheader("💰 Prime d'assurance")
    st.success(f"{prime:,.0f} FCFA")

    # =========================
    # SAVE DB
    # =========================
    save_client(age, revenu_total, couverture, risk, prime)
    st.success("Client enregistré avec succès ✅")

    # =========================
    # 📊 EXPORT EXCEL
    # =========================
    df_export = pd.DataFrame([{
        "Age": age,
        "Sexe": sexe,
        "Revenu": revenu_total,
        "Couverture": couverture,
        "Risque": risk,
        "Prime": prime,
        "Date": datetime.now()
    }])

    buffer = io.BytesIO()
    df_export.to_excel(buffer, index=False)

    st.download_button(
        "📥 Télécharger Excel",
        data=buffer,
        file_name="assurance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =========================
    # 📄 EXPORT PDF
    # =========================
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "RAPPORT ASSURANCE", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Revenu: {revenu_total}", ln=True)
    pdf.cell(200, 10, f"Couverture: {couverture}", ln=True)
    pdf.cell(200, 10, f"Risque: {risk}%", ln=True)
    pdf.cell(200, 10, f"Prime: {prime}", ln=True)

    pdf_output = pdf.output(dest="S").encode("latin1")

    st.download_button(
        "📄 Télécharger PDF",
        data=pdf_output,
        file_name="assurance_report.pdf",
        mime="application/pdf"
    )

# =========================
# 📊 ADMIN
# =========================
st.header("📊 Dashboard Admin")

data = get_clients()

df = pd.DataFrame(data, columns=[
    "ID", "Âge", "Revenu", "Couverture", "Risque", "Prime", "Date"
])

st.dataframe(df)
st.bar_chart(df["Risque"])