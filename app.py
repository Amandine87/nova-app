import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova Test")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # On configure avec le transport standard
    genai.configure(api_key=api_key, transport='rest')
    # On utilise le nom complet du modèle stable
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("Clé manquante dans les Secrets.")
    st.stop()

st.title("🚀 Nova : Test final")

user_input = st.text_input("Dis quelque chose à Nova :")

if st.button("Lancer le test"):
    try:
        response = model.generate_content(user_input)
        st.write("### Réponse de Nova :")
        st.success(response.text)
    except Exception as e:
        st.error(f"Erreur : {e}")
