import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Nova - Ton Coach Révision", page_icon="🎓")

# --- CONNEXION À L'IA ---
# On va chercher la clé API dans les secrets de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Oups ! La clé API est manquante dans les réglages de l'app.")

model = genai.GenerativeModel('gemini-1.5-flash')

# --- INTERFACE ---
st.title("🎓 Nova : Ton compagnon de révision")
st.markdown("---")

niveau = st.sidebar.radio("Ton niveau :", ["Collège (Cool)", "Lycée (Sérieux)"])

# Personnalisation du tuteur selon le niveau
if niveau == "Collège (Cool)":
    prompt_systeme = "Tu es un grand frère coach. Ton but est d'aider l'élève à trouver la réponse par lui-même. Utilise des emojis, sois encourageant. Ne donne jamais la réponse directement, pose des questions pour le guider."
    st.write("### Salut ! 👋 Prêt à décrocher tes badges ?")
else:
    prompt_systeme = "Tu es un mentor académique sérieux et structuré. Aide l'élève de lycée à comprendre la méthodologie. Sois précis et exigeant tout en restant bienveillant."
    st.write("### Bonjour. Quelle notion allons-nous approfondir ?")

user_input = st.text_area("Ta demande :", placeholder="Ex: Je n'ai pas compris comment marchent les volcans...")

if st.button("Demander de l'aide"):
    if user_input:
        with st.spinner("Nova réfléchit..."):
            try:
                # On envoie la demande à l'IA avec les instructions de ton "Tuteur"
                reponse = model.generate_content(f"Instructions : {prompt_systeme} \n\n Question de l'élève : {user_input}")
                st.write(reponse.text)
                
                if niveau == "Collège (Cool)":
                    st.success("🏆 Badge 'Curiosité' débloqué !")
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
    else:
        st.warning("Dis-moi ce que tu veux réviser !")
