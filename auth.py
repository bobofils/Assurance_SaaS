import streamlit as st
from database import create_user, get_user
from security import check_password

# =========================
# AUTH PAGE (PRO SAFE)
# =========================
def auth_page():

    st.title("🔐 Authentification SaaS")

    menu = st.radio("Menu", ["Login", "Signup"])

    # =========================
    # SIGNUP
    # =========================
    if menu == "Signup":
        st.subheader("Créer un compte")

        username = st.text_input("Utilisateur", key="su_user")
        password = st.text_input("Mot de passe", type="password", key="su_pass")

        if st.button("Créer compte"):

            if username == "" or password == "":
                st.warning("⚠️ Champs obligatoires")
                return

            success = create_user(username, password)

            if success:
                st.success("Compte créé avec succès ✅")
            else:
                st.error("Utilisateur déjà existant ❌")

    # =========================
    # LOGIN
    # =========================
    else:
        st.subheader("Connexion")

        username = st.text_input("Utilisateur", key="li_user")
        password = st.text_input("Mot de passe", type="password", key="li_pass")

        if st.button("Se connecter"):

            if username == "" or password == "":
                st.warning("⚠️ Remplis tous les champs")
                return

            user = get_user(username)

            if user is None:
                st.error("Utilisateur introuvable ❌")
                return

            # user[2] = password hash
            if check_password(password, user[2]):

                st.session_state["user"] = username
                st.success("Connexion réussie ✅")

                st.rerun()

            else:
                st.error("Mot de passe incorrect ❌")