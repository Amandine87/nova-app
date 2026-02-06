import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. STYLE ET CONFIG
st.set_page_config(page_title="Nova Vision", page_icon="🎓")

# 2. CONNEXION (Plus robuste)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé API manquante.")
    st.stop()

# 3. DÉTECTION DU MODÈLE (Version simplifiée pour éviter l'erreur 404)
@st.cache_resource
def get_model():
    # On force le nom complet qui fonctionne souvent mieux
    return genai.GenerativeModel('models/gemini-1.5-flash')

model = get_model()

# 4. BARRE LATÉRALE
with st.sidebar:
    st.title("⚙️ Options")
    niveau = st.selectbox("Niveau", ["Primaire", "Collège", "Lycée"])
    uploaded_file = st.file_uploader("Importer un exercice", type=['png', 'jpg', 'jpeg'])
    if st.button("Effacer tout"):
        st.session_state.messages = []
        st.rerun()

# 5. GESTION DES MESSAGES
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✨ Nova Vision")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# 6. ENVOI ET RÉPONSE
if prompt := st.chat_input("Ta question sur l'exercice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_content = [f"Tu es Nova, tutrice niveau {niveau}. Pédagogie max.", prompt]
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
                st.image(img, width=250)

            # Utilisation d'un spinner pour faire patienter
            with st.spinner("Nova analyse le document..."):
                response = model.generate_content(full_content)
                text_response = response.text
                
            st.write(text_response)
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
