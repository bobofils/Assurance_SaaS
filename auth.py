import streamlit as st

USERS = {
    "admin": "admin123",
    "agent": "agent123"
}

def login():
    st.sidebar.title("🔐 Connexion")

    user = st.sidebar.text_input("Utilisateur")
    pwd = st.sidebar.text_input("Mot de passe", type="password")

    if st.sidebar.button("Connexion"):
        if user in USERS and USERS[user] == pwd:
            st.session_state["user"] = user
            st.success("Connexion réussie ✅")
            return True
        else:
            st.error("Login incorrect ❌")
            return False

    return False