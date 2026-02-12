import streamlit as st
import requests
import re
import os
from streamlit_mermaid import st_mermaid
import random

# Configuration de l'URL du backend
API_URL = "http://127.0.0.1:8000/chat"


st.set_page_config(
    page_title="TN-GPT",
    page_icon="",
    layout="wide"
)

# --- FONCTION UTILITAIRE POUR EXTRAIRE LE MERMAID ---
def split_response(text):
    """
    Sépare le texte explicatif du code Mermaid s'il existe.
    Renvoie un tuple (texte_propre, code_mermaid_ou_none)
    """
    pattern = r"```mermaid\s+(.*?)\s+```"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        mermaid_code = match.group(1)
        text_without_code = re.sub(pattern, "", text, flags=re.DOTALL).strip()
        return text_without_code, mermaid_code
    return text, None

def apply_dhda_design():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Masquer éléments Streamlit */
    .stAppDeployButton { display: none !important; }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] { display: none !important; }
    header {
        background-color: rgba(0,0,0,0) !important;
        border-bottom: none !important;
    }
    
    /* Variables couleurs TELECOM Nancy */
    :root { 
        --telecom-orange: #ef7540;
        --telecom-dark: #212121;
        --telecom-light: #ffffff;
    }
    
    /* Typographie globale */
    html, body, [class*="css"] { 
        font-family: 'Roboto', sans-serif; 
        color: #333333; 
    }
    
    .stApp { 
        background-color: #FFFFFF; 
    }
    
    /* En-têtes style TELECOM Nancy */
    h1 {
        color: var(--telecom-dark) !important;
        font-weight: 700 !important;
        border-bottom: 3px solid var(--telecom-orange);
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    
    h2 {
        color: var(--telecom-orange) !important;
        font-weight: 600 !important;
    }
    
    /* Boutons style TELECOM Nancy */
    .stButton>button {
        border-radius: 5px !important;
        border: none !important;
        color: white !important;
        background-color: var(--telecom-orange);
        transition: all 0.3s ease;
        font-weight: 500;
        padding: 10px 25px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background-color: #d96330 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(239, 117, 64, 0.3);
    }
    
    /* Champ de saisie */
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--telecom-orange) !important;
        box-shadow: 0 0 0 1px var(--telecom-orange);
    }
    
    /* Messages du chat */
    .stChatMessage {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--telecom-dark);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Slider */
    .stSlider>div>div>div {
        background-color: var(--telecom-orange) !important;
    }
</style>
    """, unsafe_allow_html=True)

apply_dhda_design()
#st.image("./logo_DHDA.png", width=250)
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "static", "ducky_cassis.png")
st.image(image_path, width=200)
st.title("Bonjour, je suis TN-GPT")
messages = [
    ("Qu'avez-vous à dire pour votre défense ?", 10),
    ("Envie de jiguer, pas vous ?", 15),
    ("En date avec Crazy François",15),
    ("* en train de barboter dans l'évier cancéreux du bar *",20),
    ("on vient de me barouder aled",7),
    ("ici ça bz",5),
    ("Je ne suis pas un projet de TNS (mdr)",5),
    ("on m'a forcé à prendre du thé", 5),
    ("nique le cheval whatsapp", 15),
    ("after chez camille", 5),
    ("Prompt injection et tu vas repartir mal mon compaing", 7)
]
quotes = [mess[0] for mess in messages]
proba_messages = [mess[1] for mess in messages]
print(proba_messages)
st.write("### " + "".join(random.choices(quotes, weights =  proba_messages, k=1)))

# --- SIDEBAR AVEC LE SÉLECTEUR DE PROFIL ---
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image(os.path.join(current_dir, "static", "logo_ceten.png"), width=200)
    with col2:
        st.image(os.path.join(current_dir, "static", "logo_neuratn.png"), width=65)
    st.markdown("### Je sers à plein de choses")
    st.write("""
    - Retrouvez des infos du drive 1A
    - Découvrir le lore de TN
    - Vous donner les salles libres à l'heure actuelle
    """)

    st.divider()
    
    st.subheader("vous gros baiser vous ?")
    # Le sélecteur de persona

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Si c'est un message assistant, on vérifie s'il y a du mermaid
        if message["role"] == "assistant":
            text, mermaid = split_response(message["content"])
            st.markdown(text)
            if mermaid:
                st_mermaid(mermaid, height=300) # Tu peux ajuster la hauteur
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("Donne 5 raisons de se gooner en public (urgent)"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Attends, je réfléchis à ta question de golmon"):
            try:
                # Ajout du profil dans la requête
                payload = {
                    "question": prompt, 
                    "thread_id": "streamlit_session"
                }
                
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    raw_response = data.get("response", "Erreur: QI détecté en-dessous du premier quartile")
                    
                    # 1. On sépare le texte du graphique
                    text_content, mermaid_code = split_response(raw_response)
                    
                    # 2. On affiche le texte
                    st.markdown(text_content)
                    
                    # 3. On affiche le diagramme si présent
                    if mermaid_code:
                        st_mermaid(mermaid_code, height=350)
                    
                    st.session_state.messages.append({"role": "assistant", "content": raw_response})
                else:
                    st.error(f"Erreur API ({response.status_code}) : {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("Impossible de se connecter au backend sur le port 8000.")
            except Exception as e:
                st.error(f"Erreur : {str(e)}")