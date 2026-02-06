import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Nova : Tutrice Intelligente", page_icon="🎓", layout="centered")

# --- 2. CONNEXION API & MODÈLE ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les secrets Streamlit.")
    st.stop()

@st.cache_resource
def get_model():
    # Détection automatique du meilleur modèle disponible (évite l'erreur 404)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash_models = [m for m in models if "flash" in m]
        model_name = flash_models[0] if flash_models else models[0]
        return genai.GenerativeModel(model_name)
    except Exception:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- 3. FONCTION AUDIO (gTTS) ---
def create_audio(text):
    tts = gTTS(text=text, lang='fr')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    return audio_buffer

# --- 4. BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("🚀 Menu Nova")
    niveau = st.selectbox("Niveau scolaire", ["Primaire", "Collège", "Lycée", "Supérieur"])
    
    st.write("---")
    st.write("📷 **Analyse de document**")
    uploaded_file = st.file_uploader("Envoie une photo de ton cours/exercice", type=['png', 'jpg', 'jpeg'])
    
    st.write("---")
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# --- 5. INITIALISATION DE LA MÉMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova : Ta Tutrice")
st.caption(f"Connectée • Niveau : {niveau} • Modèle : {model.model_name}")

# --- 6. AFFICHAGE DES MESSAGES ---
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        # Si c'est Nova qui parle, on propose d'écouter
        if m["role"] == "assistant":
            if st.button(f"🔊 Écouter", key=f"btn_{i}"):
                audio_file = create_audio(m["content"])
                st.audio(audio_file, format='audio/mp3')

# --- 7. ZONE DE CHAT ET LOGIQUE ---
if prompt := st.chat_input("Pose ta question ici..."):
    # On ajoute le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de Nova
    with st.chat_message("assistant"):
        try:
            # Préparation du contexte
            instruction = f"Tu es Nova, une tutrice pour le niveau {niveau}. Sois très pédagogue, encourageante, et n'hésite pas à décomposer tes explications."
            contenu = [instruction, prompt]
            
            # Si une image est présente
            if uploaded_file:
                image = Image.open(uploaded_file)
                conten
