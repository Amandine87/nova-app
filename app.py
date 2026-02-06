import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page (Apparence)
st.set_page_config(page_title="Nova - Ton Coach Révision", page_icon="🎓", layout="centered")

# 2. Connexion sécurisée à l'IA de Google
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Configuration incomplète : Clé API introuvable dans les Secrets de Streamlit.")
    st.stop()

# 3. Barre latérale : Choix du niveau
st.sidebar.title("Configuration")
niveau = st.sidebar.radio("Ton niveau scolaire :", ["Collège (Coach Cool)", "Lycée (Mentor Sérieux)"])

# 4. Personnalisation du comportement de Nova
if niveau == "Collège (Coach Cool)":
    nom_coach = "Nova 🚀"
    instruction_ia = "Tu es Nova, un grand frère coach pour collégien. Ton but est d'aider l'élève à comprendre par lui-même. Utilise des emojis, sois très encourageant, et ne donne JAMAIS la réponse directement. Pose des questions progressives."
    message_accueil = "Salut ! 👋 Prêt à relever le défi du jour ? Quel sujet te pose problème ?"
else:
    nom_coach = "Nova Académie 🏛️"
    instruction_ia = "Tu es Nova, un mentor académique pour lycéen. Aide à comprendre la méthodologie et les concepts complexes. Ton ton est sérieux, structuré, mais bienveillant. Focalise-toi sur la logique et la rigueur."
    message_accueil = "Bonjour. Quelle notion ou méthodologie souhaitez-vous approfondir aujourd'hui ?"

# 5. Interface principale
st.title(f"🎓 {nom_coach}")
st.write(message_accueil)
st.markdown("---")

# Zone de saisie de l'élève
user_input = st.text_area("Explique-moi ce que tu révises :", placeholder="Ex: Je ne comprends pas le cycle de l'eau...")

if st.button("Demander de l'aide
