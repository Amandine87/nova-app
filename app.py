import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Import de la voix
try:
    from gtts import gTTS
    voice_ok = True
except:
    voice_ok = False

st.set_page_config(page_title="Nova", page_icon="🎓")

# --- CONNEXION SÉCURISÉE ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# --- SÉLECTION DU MODÈLE (ANTI-404) ---
@st.cache_resource
def load_model():
    # Liste des noms que Google utilise selon les régions/comptes
    noms_possibles = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'models/gemini-1.5-flash',
        'gemini-pro-vision'
    ]
    
    for nom in noms_possibles:
        try:
            m = genai.GenerativeModel(nom)
            # Petit test rapide pour voir si le modèle répond
            return m
        except:
            continue
    return genai.GenerativeModel('gemini-pro') # Dernier recours

model = load_model()

# --- INTERFACE ---
st.title("✨ Nova : Aide aux devoirs")

with st.sidebar:
    st.info(f"Modèle : {model.model_name}")
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Réinitialiser la discussion"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])

# --- ACTION ---
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Préparation du contenu
            content = [prompt]
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=250)
                content.append(img)
            
            # Génération de la réponse
            response = model.generate_content(content)
            txt = response.text
            
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            # Audio
            if voice_ok and txt:
                tts = gTTS(text=txt, lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
                
        except Exception as e:
            st.error(f"Erreur technique : {e}")
            st.info("Conseil : Si l'erreur persiste, essaie de rafraîchir la page.")
