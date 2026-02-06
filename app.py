import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Nova Test")

# Connexion directe
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # On utilise le modèle 1.5-flash-latest qui est le plus moderne
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Désolé, je ne trouve toujours pas la clé dans les Secrets.")
    st.stop()

st.title("🚀 Nova : Test de connexion")

user_input = st.text_input("Dis quelque chose à Nova :")

if st.button("Lancer le test"):
    try:
        response = model.generate_content(user_input)
        st.write("### Réponse de Nova :")
        st.success(response.text)
    except Exception as e:
        st.error(f"Erreur : {e}")
        
