import streamlit as st
import google.generativeai as genai

# On récupère la clé proprement
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Si le format [general] a été utilisé
    api_key = st.secrets.general["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

st.title("Test Nova 🚀")

prompt = st.text_input("Dis-moi 'Coucou' :")

if st.button("Envoyer"):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.success(response.text)
    except Exception as e:
        st.error(f"Zut, l'erreur est : {e}")
