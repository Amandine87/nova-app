import streamlit as st
import google.generativeai as genai

# 1. PERSONNALISATION DU DESIGN (CSS)
st.set_page_config(page_title="Nova Éducation", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    /* Modifier la couleur de fond générale */
    .stApp {
        background: linear-gradient(to bottom, #f0f2f6, #ffffff);
    }
    
    /* Personnaliser les titres */
    h1 {
        color: #2e4a7d;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Style de la barre latérale */
    section[data-testid="stSidebar"] {
        background-color: #e3e9f2;
    }
    
    /* Style des messages du chat */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE
with st.sidebar:
    st.title("🎓 Espace Étude")
    niveau = st.selectbox("Niveau de l'élève", [
        "Primaire (CP-CM2)", 
        "Collège (6ème-3ème)", 
        "Lycée (Seconde-Terminale)", 
        "Études Supérieures"
    ])
    st.markdown("---")
    generer_quiz = st.button("🎯 Me donner un exercice !")
    if st.button("🗑️ Effacer la leçon"):
        st.session_state.messages = []
        st.rerun()

# 3. CONNEXION ET MODÈLE (Inchangé)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return genai.GenerativeModel(available_models[0] if available_models else 'gemini-1.5-flash')

model = load_model()

# 4. INTERFACE
st.title("✨ Nova : Ta Tutrice")
st.caption(f"Mode d'apprentissage actif activé • Niveau : {niveau}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIQUE QUIZ
if generer_quiz:
    with st.chat_message("assistant"):
        if not st.session_state.messages:
            st.info("Dis-moi d'abord ce que tu veux apprendre !")
        else:
            prompt_quiz = f"Basé sur notre historique, propose un court exercice niveau {niveau}. Pas de réponse immédiate."
            response = model.generate_content(prompt_quiz)
            st.markdown("### 📝 Ton petit défi :")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": f"📝 DÉFI : {response.text}"})

# 6. DISCUSSION
if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        system_instruction = f"Tu es Nova, tutrice pour le niveau {niveau}. Sois pédagogue, utilise des exemples concrets et encourage l'élève."
        history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        response = model.generate_content(f"{system_instruction}\n\n{history}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
