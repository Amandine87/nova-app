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

# --- CONNEXION ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# --- SÉLECTION DU MODÈLE ---
@st.cache_resource
def find_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        name = next((m for m in models if "flash" in m), models[0])
        return genai.GenerativeModel(name)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = find_model()

# --- INTERFACE ---
st.title("✨ Nova : Aide aux devoirs")

with st.sidebar:
    st.info(f"Modèle : {model.model_name}")
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Réinitialiser"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])

# --- COEUR DU PROGRAMME ---
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            content = [f"Tu es Nova, tutrice. Aide sur : {prompt}"]
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=250)
                content.append(img)
            
            response = model.generate_content(content)
            txt = response.text
            
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            if voice_ok and txt:
                tts = gTTS(text=txt, lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
        except Exception as e:
            st.error(f"Erreur : {e}")
