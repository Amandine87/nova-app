import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Nova - Ton Coach Révision", page_icon="🎓")

# Connexion à l'IA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Configuration incomplète : Clé API introuvable.")
    st.stop()

# Barre latérale
st.sidebar.title("Configuration")
niveau = st.sidebar.radio("Ton niveau :", ["Collège (Cool)", "Lycée (Sérieux)"])

# Personnalisation
if niveau == "Collège (Cool)":
    prompt_systeme = "Tu es Nova, un coach pour collégien. Aide l'élève par étapes. Ne donne pas la réponse directe."
    st.title("🎓 Nova 🚀")
    st.write("Salut ! Quel sujet on explore aujourd'hui ?")
else:
    prompt_systeme = "Tu es Nova, un mentor pour lycéen. Sois structuré et précis."
    st.title("🎓 Nova Académie 🏛️")
    st.write("Bonjour. Quelle notion souhaitez-vous approfondir ?")

# Interface de saisie
user_input = st.text_area("Ta demande :", placeholder="Ex: Je ne comprends pas les fractions...")

if st.button("Demander de l'aide"):
    if user_input:
        with st.spinner("Nova réfléchit..."):
            try:
                response = model.generate_content(f"{prompt_systeme}\nQuestion: {user_input}")
                st.markdown("---")
                st.info(response.text)
                if niveau == "Collège (Cool)":
                    st.balloons()
            except Exception as e:
                st.error(f"Erreur technique : {e}")
    else:
        st.warning("Écris quelque chose d'abord !")
