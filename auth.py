import streamlit as st
from database import create_user, get_user
from security import check_password


def auth_page():

    st.title("🔐 Auth SaaS PRO")

    menu = st.radio("Menu", ["Login", "Signup"])

    # =========================
    # SIGNUP
    # =========================
    if menu == "Signup":

        username = st.text_input("Utilisateur", key="su_user")
        password = st.text_input("Mot de passe", type="password", key="su_pass")

        if st.button("Créer compte"):

            if username == "" or password == "":
                st.warning("Champs obligatoires")
                return

            if create_user(username, password):
                st.success("Compte créé ✅")
            else:
                st.error("Utilisateur déjà existant ❌")

    # =========================
    # LOGIN
    # =========================
    else:

        username = st.text_input("Utilisateur", key="li_user")
        password = st.text_input("Mot de passe", type="password", key="li_pass")

        if st.button("Se connecter"):

            user = get_user(username)

            if user is None:
                st.error("Utilisateur introuvable ❌")
                return

            if check_password(password, user[2]):

                st.session_state["user"] = username
                st.success("Connexion réussie ✅")
                st.rerun()

            else:
                st.error("Mot de passe incorrect ❌")