import streamlit as st

USERS = {
    "admin": "admin123",
    "agent": "agent123"
}

def login():
    st.sidebar.title("🔐 Connexion")

    # ✅ Si déjà connecté → passer directement
    if "user" in st.session_state:
        return True

    user = st.sidebar.text_input("Utilisateur")
    pwd = st.sidebar.text_input("Mot de passe", type="password")

    if st.sidebar.button("Connexion"):
        if user in USERS and USERS[user] == pwd:
            st.session_state["user"] = user
            st.success("Connexion réussie ✅")

            # 🔥 TRÈS IMPORTANT
            st.rerun()

        else:
            st.error("Login incorrect ❌")

    return False