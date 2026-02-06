import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Tentative d'importation sécurisée de gTTS
try:
    from gtts import gTTS
    voice_available = True
except ImportError:
    voice_available = False

# --- CONFIGURATION ---
st.set_page_config(page_title="Nova", page_icon="🎓")

# --- API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

@st.cache_resource
def get_model():
    try:
        # Détection auto du modèle pour éviter l'erreur 404
        m_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = next((m for m in m_list if "flash" in m), m_list[0])
        return genai.GenerativeModel(name)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.title("Options Nova")
    lvl = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer tout"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova : Ta Tutrice")

# --- AFFICHAGE ---
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant" and voice_available:
            if st.button("🔊 Écouter", key=f"v_{i}"):
                tts = gTTS(text=m["content"], lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')

# --- LOGIQUE ---
if prompt := st.chat_input("Ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            ctx = [f"Tu es Nova, tutrice {lvl}. Sois pédagogue.", prompt]
            if img_file:
                image = Image.open(img_file)
                ctx.append(image)
                st.image(image, width=250)
            
            res = model.generate_content(ctx)
            txt = res.text
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            if voice_available:
                tts = gTTS(text=txt, lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
            else:
                st.warning("La synthèse vocale est en cours d'installation, elle sera prête bientôt !")
                
        except Exception as e:
            st.error(f"Erreur : {e}")
