import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. DESIGN ET CONFIGURATION
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
    uploaded_file = st.file_uploader("Prends en photo ton exercice", type=['png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    if st.button("🗑️ Effacer la leçon"):
        st.session_state.messages = []
        st.rerun()

# 3. CONNEXION API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_model():
    # On utilise gemini-1.5-flash qui est excellent pour la vision
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

# 4. INTERFACE
st.title("✨ Nova : Aide aux devoirs")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIQUE DE CHAT ET VISION
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Préparation du contexte pédagogique
            instructions = f"Tu es Nova, tutrice {niveau}. Aide l'élève de manière pédagogique."
            
            content_to_send = [instructions, prompt]
            
            # SI UN FICHIER EST TÉLÉCHARGÉ
            if uploaded_file is not None:
                img = Image.open(uploaded_file)
                content_to_send.append(img)
                st.image(img, caption="Document analysé", width=300)
            
            # Envoi à Gemini
            response = model.generate_content(content_to_send)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Erreur : {e}")
