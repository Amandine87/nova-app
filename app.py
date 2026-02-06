import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Nova", page_icon="🎓")

# --- API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

@st.cache_resource
def get_model():
    try:
        # On cherche un modèle qui fonctionne avec la vision
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = next((m for m in models if "flash" in m), models[0])
        return genai.GenerativeModel(name)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- AUDIO ---
def speak(text):
    if text and len(text.strip()) > 0:
        try:
            tts = gTTS(text=text, lang='fr')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            return fp
        except:
            return None
    return None

# --- UI ---
with st.sidebar:
    st.title("Options")
    lvl = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer tout"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova : Ta Tutrice")

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button("🔊 Écouter", key=f"v_{i}"):
                aud = speak(m["content"])
                if aud: st.audio(aud, format='audio/mp3')

# --- LOGIQUE ---
if prompt := st.chat_input("Ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            ctx = [f"Tu es Nova, tutrice {lvl}. Pédagogie douce.", prompt]
            if img_file:
                image = Image.open(img_file)
                ctx.append(image)
                st.image(image, width=250)
            
            res = model.generate_content(ctx)
            txt = res.text
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            # Génération audio automatique
            aud = speak(txt)
            if aud: st.audio(aud, format='audio/mp3')
        except Exception as e:
            st.error(f"Erreur : {e}")
