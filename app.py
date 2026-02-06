import streamlit as st
import google.generativeai as genai

st.title("🚀 Nova : Test Final")

# Connexion
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Utilisation du modèle pro qui est le plus stable
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Clé manquante.")
    st.stop()

user_input = st.text_input("Dis 'Bonjour' :")

if st.button("Envoyer"):
    try:
        response = model.generate_content(user_input)
        st.success(response.text)
    except Exception as e:
        st.error(f"Erreur : {e}")
