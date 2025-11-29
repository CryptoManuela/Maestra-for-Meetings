# 🎙️ Maestra for Meetings

Eine elegante App zur Verarbeitung von Meeting-Aufnahmen.

**Erstellt für Manuela Ruppert Consulting**

---

## ✨ Funktionen

- 📝 **Transkription** - Wandelt Audio in Text um (mit OpenAI Whisper)
- 📋 **Zusammenfassung** - Erstellt Zusammenfassungen nach Call-Art
- 🖼️ **Infografik** - Generiert ein Thumbnail im 16:9 Format

---

## 🚀 Installation

### Voraussetzungen

1. **Python 3.9+** installiert ([Download hier](https://python.org))
2. **OpenAI API Key** ([Holen hier](https://platform.openai.com/api-keys))
3. **Google Gemini API Key** ([Holen hier](https://makersuite.google.com/app/apikey))

### Schritt-für-Schritt

1. **API Keys einrichten:**
   - Kopiere die Datei `.env.example` und benenne sie um zu `.env`
   - Trage deine API Keys in die `.env` Datei ein

2. **App starten:**
   - **Windows:** Doppelklick auf `starte_maestra.bat`
   - **Mac/Linux:** Terminal öffnen, `./starte_maestra.sh` ausführen

3. **Fertig!** Die App öffnet sich automatisch im Browser.

---

## 📁 Projektstruktur

```
Maestra-for-Meetings/
├── app.py                 # Hauptanwendung
├── requirements.txt       # Python-Abhängigkeiten
├── .env                   # API Keys (nicht im Git!)
├── .env.example          # Vorlage für API Keys
├── starte_maestra.bat    # Startdatei für Windows
├── starte_maestra.sh     # Startdatei für Mac/Linux
├── assets/
│   └── logo.png          # Dein Logo
└── README.md             # Diese Datei
```

---

## 🎨 Branding

- **Hauptfarbe:** #c01f8f
- **Logo:** Lege dein Logo als `assets/logo.png` ab

---

## © Copyright

Manuela Ruppert Consulting
[manuela-ruppert.de](https://manuela-ruppert.de)
