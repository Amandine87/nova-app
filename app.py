import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova")

# Récupération de la clé
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # FORCE la version v1 (stable) au lieu de v1beta
    genai.configure(
        api_key=api_key,
        client_options={'api_endpoint': 'generativelanguage.googleapis.com'}
    )
    
    # On définit le modèle avec son nom court
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Clé manquante dans les Secrets.")
    st.stop()

st.title("🚀 Nova : Connexion Stable")

user_input = st.text_input("Ton message pour Nova :")

if st.button("Envoyer"):
    try:
        # On force l'appel sur la version stable
        response = model.generate_content(user_input)
        st.write("### Réponse de Nova :")
        st.success(response.text)
    except Exception as e:
        st.error(f"Détail de l'erreur : {e}")
        st.info("Astuce : Si l'erreur 404 persiste, c'est que la clé doit être recréée dans le projet par défaut.")
