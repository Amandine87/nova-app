import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Essayer d'importer la voix sans faire planter l'app
try:
    from gtts import gTTS
    voice_enabled = True
except:
    voice_enabled = False

st.set_page_config(page_title="Nova", page_icon="🎓")

# Connexion sécurisée
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # On utilise flash qui consomme moins de quota
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Ta clé API n'est pas configurée dans les Secrets.")
    st.stop()

st.title("✨ Nova : Session d'étude")

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage simple
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Zone d'envoi
with st.sidebar:
    st.info("💡 Si Nova s'arrête, attends 1 minute avant de reposer une question.")
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Réinitialiser"):
        st.session_state.messages = []
        st.rerun()

if prompt := st.chat_input("Ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # On prépare le contenu
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=250)
                full_query = [prompt, img]
            else:
                full_query = [prompt]
            
            # Appel à Google
            response = model.generate_content(full_query)
            txt = response.text
            
            st.write(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            
            # Audio uniquement si le texte a été généré
            if voice_enabled and txt:
                tts = gTTS(text=txt, lang='fr')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Trop de questions d'un coup ! Attends 1 minute avant de recommencer.")
            else:
                st.error(f"Oups, petite erreur : {e}")
