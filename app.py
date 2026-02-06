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

# --- DÉTECTION DYNAMIQUE (ANTI-404) ---
@st.cache_resource
def find_working_model():
    try:
        # On demande à Google la liste des modèles utilisables sur TON compte
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priorité : 1. Flash (rapide), 2. Pro, 3. Le premier de la liste
        for m_name in available_models:
            if "1.5-flash" in m_name: return genai.GenerativeModel(m_name)
        for m_name in available_models:
            if "pro" in m_name: return genai.GenerativeModel(m_name)
        
        return genai.GenerativeModel(available_models[0])
    except Exception as e:
        # Si même la liste échoue, on tente le nom standard sans le préfixe 'models/'
        return genai.GenerativeModel('gemini-1.5-flash')

model = find_working_model()

# --- INTERFACE ---
st.title("✨ Nova : Aide aux devoirs")

with st.sidebar:
    st.info(f"Modèle actif : {model.model_name}")
    img_file = st.file_uploader("Photo de l'exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Réinitialiser"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

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
            content = [f"Tu es Nova, une tutrice pédagogue. Aide l'élève sur : {prompt}"]
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=250)
                content.append(img)
            
            # Génération
            response = model
