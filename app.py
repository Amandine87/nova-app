import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION ET STYLE
st.set_page_config(page_title="Nova Audio", page_icon="🎓")

# PETIT SCRIPT POUR LA LECTURE VOCALE
st.markdown("""
    <script>
    function speak(text) {
        window.speechSynthesis.cancel(); // Arrête toute lecture en cours
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'fr-FR'; // Force la voix française
        window.speechSynthesis.speak(utterance);
    }
    </script>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #f4f7f9, #ffffff); }
    [data-testid="stChatMessage"] { border-radius: 15px; }
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONNEXION ET MODÈLE
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

# 5. AFFICHAGE DES MESSAGES + BOUTON AUDIO
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        # On ajoute un bouton audio uniquement pour les réponses de Nova
        if m["role"] == "assistant":
            if st.button(f"🔊 Écouter", key=f"audio_{i}"):
                # On utilise un petit hack Streamlit pour appeler la fonction JS
                st.components.v1.html(f"<script>window.parent.speak({repr(m['content'])})</script>", height=0)

# 6. LOGIQUE DE CHAT
if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            instructions = f"Tu es Nova, tutrice {niveau}. Réponds de façon claire et encourageante."
            full_content = [instructions, prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250)

            with st.spinner("Nova prépare sa réponse..."):
                response = model.generate_content(full_content)
                res_text = response.text
                
            st.write(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            # Petit bouton immédiat pour le dernier message
            if st.button("🔊 Écouter cette réponse"):
                st.components.v1.html(f"<script>window.parent.speak({repr(res_text)})</script>", height=0)
                
        except Exception as e:
            st.error(f"Erreur : {e}")
