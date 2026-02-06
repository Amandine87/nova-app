import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante dans les Secrets.")
    st.stop()

st.title("🚀 Nova : Test de Connexion")

# --- LE CODE DÉTECTIVE ---
try:
    # On cherche quel modèle est disponible pour ton compte
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if available_models:
        # On prend le premier modèle disponible (souvent gemini-pro ou gemini-1.5-flash)
        selected_model = available_models[0]
        st.info(f"Modèle détecté : {selected_model}")
        model = genai.GenerativeModel(selected_model)
    else:
        st.error("Aucun modèle trouvé pour cette clé.")
        st.stop()
except Exception as e:
    st.error(f"Erreur lors de la détection : {e}")
    st.stop()
# -------------------------

user_input = st.text_input("Ton message pour Nova :")

if st.button("Envoyer"):
    try:
        response = model.generate_content(user_input)
        st.write("### Réponse :")
        st.success(response.text)
    except Exception as e:
        st.error(f"Erreur technique : {e}")
