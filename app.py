import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. DESIGN ET CONFIGURATION (CSS)
st.set_page_config(page_title="Nova Vision", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #f0f2f6, #ffffff); }
    h1 { color: #2e4a7d; font-family: 'Helvetica Neue', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #e3e9f2; }
    [data-testid="stChatMessage"] { border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE
with st.sidebar:
    st.title("🎓 Nova Vision")
    niveau = st.selectbox("Niveau de l'élève", ["Primaire", "Collège", "Lycée", "Supérieur"])
    
    st.markdown("---")
    st.write("📷 **Analyse de document**")
    # Zone pour uploader l'image
    uploaded_file = st.file_uploader("Envoie une photo de ton exercice", type=['png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# 3. CONNEXION ET DÉTECTION DU MODÈLE
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets Streamlit.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_model_detective():
    # Cette fonction cherche le nom exact du modèle sur ton compte pour éviter l'erreur 404
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if '1.5-flash' in m.name:
                    return genai.GenerativeModel(m.name)
        return genai.GenerativeModel('gemini-pro')
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = load_model_detective()

# 4. INTERFACE PRINCIPALE
st.title("✨ Nova : Aide aux devoirs")
st.caption(f"Mode Vision activé • Niveau actuel : {niveau}")

# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIQUE DE CHAT ET VISION
if prompt := st.chat_input("Pose ta question ici..."):
    # On affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown
        
