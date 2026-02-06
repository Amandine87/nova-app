import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. CONFIGURATION
st.set_page_config(page_title="Nova Audio", page_icon="🎓")

# 2. CONNEXION API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

@st.cache_resource
def get_best_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash_models = [m for m in models if "flash" in m]
        return genai.GenerativeModel(flash_models[0] if flash_models else models[0])
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_best_model()

# 3. BARRE LATÉRALE
with st.sidebar:
    st.title("⚙️ Options Nova")
    niveau = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    uploaded_file = st.file_uploader("Document à analyser", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# 4. MÉMOIRE DU CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova : Ta Tutrice Vocale")

# 5. FONCTION POUR GÉNÉRER L'AUDIO
def play_audio(text):
    tts = gTTS(text=text, lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# 6. AFFICHAGE DES MESSAGES
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            # On crée un bouton qui génère un petit lecteur audio
            if st.button(f"🔊 Préparer l'audio", key=f"btn_{i}"):
                audio_fp = play_audio(m["content"])
                st.audio(audio_fp, format='audio/mp3')

# 7. LOGIQUE DE CHAT
if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            instructions = f"Tu es Nova, tutrice {niveau}. Réponds de façon claire et courte."
            full_content = [instructions, prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250)

            with st.spinner("Nova réfléchit..."):
                response = model.generate_content(full_content)
                res_text = response.text
                
            st.write(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
            # Option audio immédiate pour la réponse
            audio_fp = play_audio(res_text)
            st.audio(audio_fp, format='audio/mp3')
                
        except Exception as e:
            st.error(f"Erreur : {e}")
