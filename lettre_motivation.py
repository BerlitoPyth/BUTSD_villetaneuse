import streamlit as st
import time
from PIL import Image
from pathlib import Path
import json
import pandas as pd
import base64
from io import BytesIO

# Définition du chemin racine du projet
project_root = Path(__file__).parent

# Import des composants essentiels uniquement
from components.theme import apply_dark_theme
from components.projet_data_explorer import display_data_explorer_project
from components.presentation import display_presentation
from components.projet_gaming import display_project_concept
from components.floating_chat import add_floating_chat_to_app  # Changé generate_response pour add_floating_chat_to_app
from components.matrix_animation import display_matrix_animation
from content.lettre_motivation_content import get_lettre_motivation_content, get_note_importante
from components.admission_prediction import (
    load_data, 
    display_summary_stats,
    display_explain_stats,
    display_prediction_interface,
    display_global_interface,
    display_conseils,
    display_profil_feedback
)

def load_css():
    """Charge les fichiers CSS"""
    css_files = [
        'typography.css',
        'layout.css',
        'components.css',
        'main.css',
        'sidebar.css'
    ]
    for css_file in css_files:
        css_path = Path(project_root) / "styles" / css_file
        try:
            print(f"Tentative de chargement de {css_path}")  # Debug
            css_content = css_path.read_text()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            print(f"Chargement réussi de {css_file}")  # Debug
        except Exception as e:
            print(f"Erreur lors du chargement de {css_file}: {e}")
            st.warning(f"Erreur de chargement du style {css_file}")

def write_text_slowly(text):
    """Fonction pour l'effet machine à écrire"""
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(f"### {text[:i]}▌")
        time.sleep(0.03)
    placeholder.markdown(f"### {text}")

# Après l'ouverture de l'image, avant l'affichage du popup
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Modifier la fonction main() pour ajouter un état de navigation
def main():
    st.set_page_config(
        page_title="Candidature BUT Science des Données",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Ajouter un container vide tout en haut avec une ancre
    scroll_to_top = st.empty()
    scroll_to_top.markdown("""
        <div id="top"></div>
    """, unsafe_allow_html=True)
    
    load_css()
    apply_dark_theme()  # Appliquer le thème sombre directement
    
    # Animation state management
    if 'matrix_done' not in st.session_state:
        st.session_state.matrix_done = False
    
    # Matrix animation at startup
    if not st.session_state.matrix_done:
        display_matrix_animation()
        st.session_state.matrix_done = True
        st.rerun()

    # Le reste du code principal (sidebar, contenu, etc.)
    with st.sidebar:
        
        st.title("🎯 Navigation")
        
        # Menu de navigation
        selection = st.radio(
            "",
            ["🏠 Accueil",
             "📄 Lettre de recommandation",  
             "📊 Data Project",
             "🔧 Projet Perso",
             "💼 Projets Pro",
             "👤 Présentation"]
        )
        
        st.session_state.selection = selection
        
        st.markdown("---")
        
        # Formations en dernier
        st.success("""
        ### 📚 Formations
        - DAEU B (en cours)
        - Python for Everybody
        - Python Data Structures
        - Using Python to Access Web Data
        - École 42 - La Piscine
        - École Nationale des Scaphandriers
        - Expérience professionnelle
        """)

    # Contenu principal basé sur la sélection
    if selection == "🏠 Accueil":
        # Création d'un container pour le titre et la photo
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
                <div style="margin: 0;">
                    <h1 style="
                        font-size: 2.5em;
                        margin: -0.5rem 0 0.25rem 0;
                        color: inherit;
                        padding: 0;
                    ">Candidature BUT Science des Données</h1>
                    <h2 style="
                        font-size: 1.5em;
                        margin: 0 0 0.5rem 0;
                        color: inherit;
                    ">Adrien BERLIAT</h2>
                    <h3 style="
                        font-size: 1.2em;
                        margin: 0 0 1rem 0;
                        color: inherit;
                    ">📧berliatadrien@gmail.com</h3>
                    <h3 style="
                        font-size: 1.2em;
                        margin: 0 0 1rem 0;
                        color: inherit;
                    ">💻innovaweb.fr</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Effet machine à écrire
            if 'title_written' not in st.session_state:
                write_text_slowly("De la profondeur des océans à la profondeur des données... 🌊➡️📊")
                st.session_state.title_written = True
            else:
                st.markdown("""
                    <h3 style="
                        font-style: italic;
                        color: inherit;
                        font-size: 1.2em;
                        margin: 0 0 2rem 0;
                    ">De la profondeur des océans à la profondeur des données... 🌊➡️📊</h3>
                """, unsafe_allow_html=True)

        # Ajouter une div conteneur avec la classe personnalisée
        with st.expander("⚠️ **Note importante**"):
            st.markdown(get_note_importante(), unsafe_allow_html=True)

    

        with col2:
            try:
                image = Image.open(".assets/photo.jpg")
                image_rotated = image.rotate(0, expand=True)
                st.image(image_rotated, width=200)
            except Exception as e:
                st.info("📸 Photo non disponible")
                print(f"Erreur: {e}")
                
        # Ajout du chat
        add_floating_chat_to_app()  # Appel correct de la fonction
        
        # Points clés
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            ### ✨ Points Clés
            - 📊 Goût pour les mathématiques
            - 🤝 Expérience du travail d'équipe
            - 💡 Autodidacte
            - 🚀 Motivation à toute épreuve
            """)
        with col2:
            st.info("""
            ### 🎓 Formation Actuelle
            - 📚 DAEU B en cours
            - 💻 Certifications Python
            - 🔍 École 42 - La Piscine
            - 🌟 Excellents résultats en sciences
            """)
            
        st.markdown("---")
        
        # Titre de la lettre de motivation avec icône
        st.markdown("""
            <h2 style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin: 1rem 0;
                line-height: 1.2;
            ">
                📜 Lettre de Motivation
            </h2>
        """, unsafe_allow_html=True)
        
        # Contenu de la lettre 
        st.markdown(get_lettre_motivation_content())

    elif selection == "👤 Présentation":

        display_presentation(show_title=False)  # Nouveau paramètre pour éviter le doublon

        
    elif selection == "🔧 Projet Perso":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0 0 1.5rem 0;
                color: inherit;
            ">🔧 Créations originales</h1>
        """, unsafe_allow_html=True)
        display_project_concept(show_title=False)  # Nouveau paramètre pour éviter le doublon
        
    elif selection == "💼 Projets Pro":
        display_data_explorer_project()
        
    elif selection == "📊 Data Project":
        try:
            df = load_data()
            
            if df is not None:
                # 1. Title
                st.markdown("""
                    <h1 style='margin-bottom: 2rem;'>
                        📊 Analyse des données Parcoursup 2024 - BUT Science des données
                    </h1>
                """, unsafe_allow_html=True)
                
                # 2. Display summary stats
                display_summary_stats(df)
                
                # 3. Show expanders
                display_explain_stats(df)

                with st.expander("ℹ️ Comment fonctionne le modèle de prédiction ?"):
                    st.markdown("""
                    ### Comment sont calculées vos chances d'admission ?

                    Le calculateur utilise un modèle basé sur les données réelles Parcoursup 2024 qui combine trois facteurs principaux :

                    #### 1. Taux de proposition de base
                    - Calculé à partir des statistiques réelles de propositions par type de Bac
                    - Utilise le ratio : nombre de propositions / nombre de candidats du même profil
                    - Prend en compte :
                        * Pour Bac général : `propositions Bac général / candidats Bac général`
                        * Pour Bac technologique : `propositions Bac techno / candidats Bac techno`
                        * Pour autres profils (DAEU...) : `propositions autres / candidats autres`

                    #### 2. Bonus Mention au Bac
                    Multiplicateur appliqué selon la mention à partir des données réelles :
                    - Sans mention : ×1.0 (pas de bonus)
                    - Assez Bien : ×1.3 (+30%)
                    - Bien : ×1.6 (+60%)
                    - Très Bien : ×2.0 (+100%)

                    #### 3. Bonus Boursier
                    - Bonus proportionnel au taux de boursiers de l'établissement
                    - Formule : `1 + max(0.1, taux_boursiers_etablissement)`
                    - Minimum garanti de 10% de bonus pour les boursiers

                    #### Calcul final
                    La probabilité finale est calculée en multipliant :
                    ```
                    Probabilité = Taux de proposition × Bonus mention × Bonus boursier
                    ```

                    #### Important à noter
                    - Les probabilités sont plafonnées à 100%
                    - Ces chances représentent la probabilité de recevoir une proposition, pas d'être accepté définitivement

                    #### Fiabilité
                    - Le modèle se base uniquement sur les données quantitatives disponibles
                    - Les éléments qualitatifs (lettre de motivation, projets personnels, etc.) peuvent influencer significativement la décision finale
                    """)
                
                # 4. Add tabs for prediction models
                tab1, tab2 = st.tabs(["🎯 Prédiction détaillée", "🌍 Comparaison globale"])
                
                with tab1:
                    st.markdown("⚠️ Ces probabilités représentent vos chances de **recevoir une proposition de l'IUT**, pas d'être accepté définitivement. Ce modèle n'est sans doute pas parfait, j'ai sûrement omis des facteurs, et c'est justement pour ça que je veux rejoindre le BUT SD ! En tout cas, j'ai pris beaucoup de plaisir à le réaliser tout comme cette application.")
                    iut_choice, probability = display_prediction_interface(df, show_title=False)
                    display_profil_feedback(probability)
                
                with tab2:
                    display_global_interface(df)
                    display_conseils(df)
                    
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")
            print(f"Erreur détaillée: {e}")

    elif selection == "📄 Lettre de recommandation":
        st.markdown("""
            <h1 style="
                font-size: 2.5em;
                margin: 0 0 1.5rem 0;
                color: inherit;
            ">📄 Lettre de recommandation</h1>
        """, unsafe_allow_html=True)
        
        # Centrer l'image
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            try:
                # Charger et afficher l'image
                lettre = Image.open(".assets/lettre_recommandation.jpg")
                st.image(lettre, width=1100)
                
            except Exception as e:
                st.error("Lettre de recommandation non disponible")
    
    # Footer
    st.markdown("---")
    st.markdown("*Application interactive créée pour accompagner ma candidature au BUT Science des Données*")

if __name__ == "__main__":
    main()