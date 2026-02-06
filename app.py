import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. CONFIGURATION
st.set_page_config(page_title="Nova : Tutrice Intelligente", page_icon="🎓")

# 2. CONNEXION API & MODÈLE (Correction 404)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante dans les secrets.")
    st.stop()

@st.cache_resource
def get_model():
    # Liste les modèles pour trouver celui qui accepte generateContent
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # On cherche gemini-1.5-flash ou gemini-pro
        selected = next((m for m in models if "1.5-flash" in m), models[0])
        return genai.GenerativeModel(selected)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# 3. FONCTION AUDIO
def create_audio(text):
    tts = gTTS(text=text, lang='fr')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    return audio_buffer

# 4. BARRE LATÉRALE
with st.sidebar:
    st.title("🚀 Menu Nova")
    niveau = st.selectbox("Niveau scolaire", ["Primaire", "Collège", "Lycée", "Supérieur"])
    st.write("---")
    st.write("📷 **Analyse de document**")
    uploaded_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

# 5. INITIALISATION MÉMOIRE
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova : Ta Tutrice")
st.caption(f"Prête à t'aider • Niveau : {niveau}")

# 6. AFFICHAGE DES MESSAGES
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 Écouter", key=f"btn_{i}"):
                audio_file = create_audio(m["content"])
                st.audio(audio_file, format='audio/mp3')

# 7. LOGIQUE DE CHAT
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Préparation du contenu (Texte + Image)
            instruction = f"Tu es Nova, une tutrice pour le niveau {niveau}. Aide l'élève de façon pédagogue sur ce document."
            contenu_final = [instruction, prompt]
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                contenu_final.append(image)
                st.image(image, width=300)

            with st.spinner("Nova analyse..."):
                response = model.generate_content(contenu_final)
                reponse_texte = response.text
            
            st.markdown(reponse_texte)
            st.session_state.messages.append({"role": "assistant", "content": reponse_texte})
            
            # Lecture audio automatique pour la nouvelle réponse
            audio_fp = create_audio(reponse_texte)
            st.audio(audio_fp, format='audio/mp3')
            
        except Exception as e:
            st.error(f"Désolé, j'ai un souci technique : {e}")
