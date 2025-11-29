# -*- coding: utf-8 -*-
"""
Maestra for Meetings
Erstellt von Manuela Ruppert Consulting
https://manuela-ruppert.de
"""

import streamlit as st
from pathlib import Path
import base64

# ============================================
# KONFIGURATION
# ============================================
APP_NAME = "Maestra for Meetings"
BRAND_COLOR = "#c01f8f"
BRAND_COLOR_LIGHT = "#e691c9"
BRAND_COLOR_DARK = "#8a1566"

# ============================================
# CUSTOM CSS FÜR SCHÖNES DESIGN
# ============================================
def load_custom_css():
    st.markdown(f"""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* Grundlegendes Styling */
        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif;
        }}

        /* Header verstecken */
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Hintergrund */
        .stApp {{
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        }}

        /* Hauptcontainer */
        .main-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Logo und Titel Container */
        .header-container {{
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}

        .app-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {BRAND_COLOR};
            margin: 1rem 0 0.5rem 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .app-subtitle {{
            font-size: 1.1rem;
            color: #666;
            font-weight: 300;
        }}

        /* Upload Box */
        .upload-container {{
            background: white;
            border-radius: 20px;
            padding: 3rem 2rem;
            box-shadow: 0 10px 40px rgba(192, 31, 143, 0.15);
            border: 2px dashed {BRAND_COLOR_LIGHT};
            text-align: center;
            margin: 2rem 0;
            transition: all 0.3s ease;
        }}

        .upload-container:hover {{
            border-color: {BRAND_COLOR};
            box-shadow: 0 15px 50px rgba(192, 31, 143, 0.25);
            transform: translateY(-2px);
        }}

        /* Call-Art Buttons */
        .call-type-container {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }}

        .call-type-card {{
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}

        .call-type-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(192, 31, 143, 0.2);
            border-color: {BRAND_COLOR};
        }}

        .call-type-card.selected {{
            border-color: {BRAND_COLOR};
            background: linear-gradient(135deg, #fff 0%, #fdf2f8 100%);
        }}

        .call-type-icon {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .call-type-title {{
            font-weight: 600;
            color: #333;
            font-size: 1.1rem;
        }}

        /* Hauptbutton */
        .stButton > button {{
            background: linear-gradient(135deg, {BRAND_COLOR} 0%, {BRAND_COLOR_DARK} 100%);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(192, 31, 143, 0.4);
            width: 100%;
            margin-top: 1rem;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(192, 31, 143, 0.5);
        }}

        /* Download Bereich */
        .download-section {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}

        .download-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: {BRAND_COLOR};
            margin-bottom: 1.5rem;
            text-align: center;
        }}

        .download-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }}

        .download-card {{
            background: linear-gradient(135deg, #fdf2f8 0%, #fff 100%);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid {BRAND_COLOR_LIGHT};
        }}

        .download-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid #eee;
            color: #666;
        }}

        .footer a {{
            color: {BRAND_COLOR};
            text-decoration: none;
            font-weight: 500;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        /* Radio Buttons verstecken und eigene Cards nutzen */
        .stRadio > div {{
            display: none;
        }}

        /* Selectbox Styling */
        .stSelectbox > div > div {{
            background: white;
            border-radius: 10px;
            border: 2px solid {BRAND_COLOR_LIGHT};
        }}

        /* Progress Bar */
        .stProgress > div > div {{
            background: linear-gradient(90deg, {BRAND_COLOR} 0%, {BRAND_COLOR_LIGHT} 100%);
        }}

        /* Info/Success/Warning Boxes */
        .stAlert {{
            border-radius: 15px;
        }}

        /* Abstand oben */
        .block-container {{
            padding-top: 2rem;
        }}

    </style>
    """, unsafe_allow_html=True)


def get_logo_html():
    """Logo anzeigen - verwendet Platzhalter wenn kein Logo vorhanden"""
    logo_path = Path("assets/logo.png")

    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{logo_data}" style="max-width: 200px; margin-bottom: 1rem;">'
    else:
        # Eleganter Platzhalter
        return f'''
        <div style="
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, {BRAND_COLOR} 0%, {BRAND_COLOR_DARK} 100%);
            border-radius: 50%;
            margin: 0 auto 1rem auto;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(192, 31, 143, 0.3);
        ">
            <span style="font-size: 3rem;">🎙️</span>
        </div>
        '''


def render_header():
    """Header mit Logo und Titel"""
    st.markdown(f"""
    <div class="header-container">
        {get_logo_html()}
        <h1 class="app-title">✨ {APP_NAME} ✨</h1>
        <p class="app-subtitle">Transkription • Zusammenfassung • Infografik</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Footer mit Copyright und Website"""
    st.markdown("""
    <div class="footer">
        <p>© Manuela Ruppert Consulting</p>
        <p><a href="https://manuela-ruppert.de" target="_blank">manuela-ruppert.de</a></p>
    </div>
    """, unsafe_allow_html=True)


def render_call_type_selector():
    """Call-Art Auswahl als schöne Cards"""
    call_types = {
        "coaching": {"icon": "🎯", "title": "Coaching Call"},
        "qa": {"icon": "❓", "title": "Q&A Call"},
        "netzwerk": {"icon": "🤝", "title": "Netzwerkgespräch"},
        "verkauf": {"icon": "💼", "title": "Verkaufsgespräch"}
    }

    # Session State für Auswahl
    if "selected_call_type" not in st.session_state:
        st.session_state.selected_call_type = None

    st.markdown("### 📋 Wähle die Call-Art:")

    cols = st.columns(2)

    for idx, (key, value) in enumerate(call_types.items()):
        col = cols[idx % 2]
        with col:
            is_selected = st.session_state.selected_call_type == key
            border_color = BRAND_COLOR if is_selected else "transparent"
            bg_color = "linear-gradient(135deg, #fff 0%, #fdf2f8 100%)" if is_selected else "white"

            if st.button(
                f"{value['icon']} {value['title']}",
                key=f"btn_{key}",
                use_container_width=True
            ):
                st.session_state.selected_call_type = key
                st.rerun()

    return st.session_state.selected_call_type


def main():
    """Hauptfunktion der App"""

    # Seiten-Konfiguration
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🎙️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS laden
    load_custom_css()

    # Header
    render_header()

    # Upload Bereich
    st.markdown("### 🎵 Audio-Datei hochladen")
    uploaded_file = st.file_uploader(
        "Ziehe deine MP3-Datei hierher oder klicke zum Auswählen",
        type=["mp3", "wav", "m4a", "ogg"],
        help="Unterstützte Formate: MP3, WAV, M4A, OGG"
    )

    if uploaded_file:
        st.success(f"✅ Datei geladen: **{uploaded_file.name}**")

        # Audio Player
        st.audio(uploaded_file)

    # Trennlinie
    st.markdown("---")

    # Call-Art Auswahl
    selected_type = render_call_type_selector()

    if selected_type:
        type_names = {
            "coaching": "Coaching Call",
            "qa": "Q&A Call",
            "netzwerk": "Netzwerkgespräch",
            "verkauf": "Verkaufsgespräch"
        }
        st.info(f"📌 Ausgewählt: **{type_names[selected_type]}**")

    # Trennlinie
    st.markdown("---")

    # Verarbeiten Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_btn = st.button(
            "🚀 JETZT VERARBEITEN",
            disabled=not (uploaded_file and selected_type),
            use_container_width=True
        )

    if not uploaded_file:
        st.warning("⬆️ Bitte lade zuerst eine Audio-Datei hoch")
    elif not selected_type:
        st.warning("📋 Bitte wähle eine Call-Art aus")

    # Verarbeitung (Platzhalter)
    if process_btn and uploaded_file and selected_type:
        with st.spinner("🔄 Verarbeitung läuft..."):
            # Fortschrittsanzeige
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Schritt 1: Transkription
            status_text.text("📝 Transkribiere Audio mit Whisper...")
            progress_bar.progress(33)

            # TODO: Hier kommt die echte Whisper-Transkription
            import time
            time.sleep(1)  # Platzhalter

            # Schritt 2: Zusammenfassung
            status_text.text("📋 Erstelle Zusammenfassung...")
            progress_bar.progress(66)
            time.sleep(1)  # Platzhalter

            # Schritt 3: Infografik
            status_text.text("🎨 Generiere Infografik...")
            progress_bar.progress(100)
            time.sleep(1)  # Platzhalter

            status_text.text("✅ Fertig!")

        # Download Bereich
        st.markdown("### 📥 Deine Downloads")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📄</div>
                <p><strong>Transkript</strong></p>
            </div>
            """, unsafe_allow_html=True)
            # TODO: Echter Download
            st.download_button(
                "⬇️ DOCX",
                data="Platzhalter - Transkript kommt hier",
                file_name="transkript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        with col2:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📋</div>
                <p><strong>Zusammenfassung</strong></p>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                "⬇️ DOCX",
                data="Platzhalter - Zusammenfassung kommt hier",
                file_name="zusammenfassung.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        with col3:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">🖼️</div>
                <p><strong>Infografik</strong></p>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                "⬇️ PNG",
                data="Platzhalter - Infografik kommt hier",
                file_name="infografik.png",
                mime="image/png",
                use_container_width=True
            )

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
