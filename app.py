import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Nova Test")

# Connexion ultra-simple
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante dans les Secrets !")

st.title("🚀 Nova : Test de connexion")

# LE CHANGEMENT ICI : On utilise 'gemini-pro'
model = genai.GenerativeModel('gemini-1.0-pro')

user_input = st.text_input("Dis quelque chose à Nova :")

if st.button("Lancer le test"):
    try:
        response = model.generate_content(user_input)
        st.write("### Réponse de Nova :")
        st.success(response.text)
    except Exception as e:
        st.error(f"Erreur : {e}")
