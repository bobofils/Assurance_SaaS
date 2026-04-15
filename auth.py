import streamlit as st
from database import create_user, get_user
from security import check_password


def auth_page():
    st.sidebar.title("🔐 Authentification")

    menu = st.sidebar.radio("Menu", ["Login", "Signup"])

    # =====================
    # SIGNUP
    # =====================
    if menu == "Signup":
        st.subheader("📝 Créer un compte")

        username = st.text_input("Nom utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Créer compte"):
            if create_user(username, password):
                st.success("Compte créé avec succès ✅")
            else:
                st.error("Utilisateur existe déjà ❌")

    # =====================
    # LOGIN
    # =====================
    if menu == "Login":
        st.subheader("🔑 Connexion")

        username = st.text_input("Utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            user = get_user(username)

            if user and check_password(password, user[2]):
                st.session_state["user"] = username
                st.success("Connexion réussie ✅")
                st.rerun()
            else:
                st.error("Identifiants incorrects ❌")