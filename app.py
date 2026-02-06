import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova Éducation", page_icon="🎓")

# 1. Barre latérale
with st.sidebar:
    st.title("🎓 Espace Étude")
    niveau = st.selectbox("Niveau de l'élève", [
        "Primaire (CP-CM2)", 
        "Collège (6ème-3ème)", 
        "Lycée (Seconde-Terminale)", 
        "Études Supérieures"
    ])
    
    st.markdown("---")
    # LE BOUTON DE QUIZ
    generer_quiz = st.button("🎯 Me donner un exercice !")
    
    if st.button("🗑️ Effacer la leçon"):
        st.session_state.messages = []
        st.rerun()

# 2. Connexion
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Clé manquante.")
    st.stop()

# 3. Modèle
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return genai.GenerativeModel(available_models[0] if available_models else 'gemini-1.5-flash')

model = load_model()

# 4. Interface
st.title(f"Nova : Ta tutrice {niveau}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIQUE DU BOUTON QUIZ ---
if generer_quiz:
    with st.chat_message("assistant"):
        try:
            prompt_quiz = f"En fonction de notre discussion précédente et du niveau {niveau}, propose-moi un seul exercice court ou une question de compréhension pour vérifier que j'ai bien compris. Ne donne pas la réponse tout de suite !"
            response = model.generate_content(prompt_quiz)
            st.markdown("### 📝 Ton petit défi :")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": f"📝 DÉFI : {response.text}"})
        except Exception as e:
            st.error(f"Erreur : {e}")

# 5. Logique de Discussion standard
if prompt := st.chat_input("Pose ta question ou réponds au quiz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = f"""
            Tu es Nova, une enseignante pédagogue pour le niveau {niveau}.
            Si l'élève répond à un exercice, corrige-le avec bienveillance.
            S'il pose une question, explique avec des exemples concrets.
            """
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            response = model.generate_content(f"{system_instruction}\n\n{history}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
