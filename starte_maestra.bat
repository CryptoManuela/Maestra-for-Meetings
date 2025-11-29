@echo off
echo.
echo ========================================
echo    MAESTRA FOR MEETINGS
echo    wird gestartet...
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo Bitte installiere Python von https://python.org
    pause
    exit /b 1
)

REM Prüfe ob virtuelle Umgebung existiert
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
    echo.
)

REM Aktiviere virtuelle Umgebung
call venv\Scripts\activate.bat

REM Installiere Abhängigkeiten falls nötig
pip install -r requirements.txt --quiet

REM Starte die App
echo.
echo App startet im Browser...
echo Druecke Strg+C zum Beenden
echo.
streamlit run app.py --server.headless true

pause
