import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova Éducation", page_icon="🎓")

# 1. Barre latérale pédagogique
with st.sidebar:
    st.title("🎓 Réglages Scolaires")
    niveau = st.selectbox("Niveau de l'élève", [
        "Primaire (CP-CM2)", 
        "Collège (6ème-3ème)", 
        "Lycée (Seconde-Terminale)", 
        "Études Supérieures"
    ])
    ton = st.select_slider("Style d'explication", options=["Simple", "Standard", "Détaillé"])
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
st.markdown(f"**Objectif :** Expliquer les concepts de manière adaptée au niveau **{niveau}**.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logique Pédagogique
if prompt := st.chat_input("Que veux-tu apprendre aujourd'hui ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # INSTRUCTIONS SYSTÈME TRÈS PRÉCISES
            system_instruction = f"""
            Tu es Nova, une enseignante bienveillante et très pédagogue. 
            Ton élève est au niveau : {niveau}.
            Tes consignes :
            1. Utilise un vocabulaire adapté à cet âge.
            2. Utilise des images, des métaphores ou des exemples concrets du quotidien.
            3. Décompose les étapes (surtout pour les maths comme les divisions).
            4. Ne donne pas juste la réponse, explique le 'pourquoi'.
            5. Style de réponse : {ton}.
            """
            
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            response = model.generate_content(f"{system_instruction}\n\nQuestion de l'élève :\n{history}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
