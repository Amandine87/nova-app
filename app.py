import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Import sécurisé
try:
    from gtts import gTTS
    voice_ok = True
except:
    voice_ok = False

st.set_page_config(page_title="Nova", page_icon="🎓")

# Connexion
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Clé API manquante.")
    st.stop()

st.title("✨ Nova : Session d'étude")

with st.sidebar:
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant" and voice_ok:
            if st.button(f"🔊 Écouter", key=f"v_{i}"):
                tts = gTTS(text=m["content"], lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)

if prompt := st.chat_input("Ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        try:
            content = [prompt]
            if img_file:
                img = Image.open(img_file)
                content.append(img)
                st.image(img, width=250)
            
            # Appel API
            response = model.generate_content(content)
            txt = response.text
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            if voice_ok:
                tts = gTTS(text=txt, lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
        except Exception as e:
            st.error(f"Erreur (Quota peut-être dépassé) : {e}")
