# BRIEFING: KI-Potenzial-Check - 100 Fragen Modell (KOSTENLOS)

## Fuer: Claude Code am MacBook zur Weiterarbeit
## Erstellt: 2026-02-15
## Status: Konzeptphase abgeschlossen, Umsetzung steht an

---

## 1. WER IST MANUELA?

**Manuela Ruppert** - KI-Strategin und Mentorin fuer selbststaendige Frauen
- Website: manuela-ruppert.de
- Kernprodukt: **KI Maestra Masterclass** (12 Wochen, Kleingruppe)
- Weitere Angebote: VIP 1:1, Community (Skool), Podcast "Mensch, KI!"
- Zielgruppe: Solo-Selbststaendige und Freiberuflerinnen (Coaches, Beraterinnen, Aerztinnen, Winzerinnen etc.)
- Primaeres KI-Tool: **Claude von Anthropic**
- Technischer Hintergrund: Vibe-Coding-Erfahrung, nutzt Claude Code

---

## 2. DIE IDEE - ZUSAMMENFASSUNG

Manuela baut den **umfassendsten KI-Potenzial-Check im DACH-Raum** - und gibt ihn **KOSTENLOS** raus.

### Kernprinzip:
- 100 Fragen in 10 Kategorien (je 10 Fragen)
- Vollautomatische Auswertung (kein manueller Aufwand fuer Manuela)
- Personalisierter Report wird per E-Mail zugestellt
- Der Check ist die EINGANGSTUER, nicht das Produkt
- Der Check oeffnet Augen und erzeugt Nachfrage nach Beratung/Masterclass

### Strategische Logik:
```
Kostenloser 100-Fragen-Check
         |
    Automatische Auswertung
    (zeigt WO Potenzial liegt)
         |
    Report per E-Mail (PDF)
         |
    CTA: "Du willst diese Hebel aktivieren?"
         |
    ┌────┴─────────────────────┐
    |                          |
    Masterclass (Gruppe)    VIP 1:1 / Workshop
    12 Wochen               Premium-Beratung
```

### Warum KOSTENLOS funktioniert:
1. **Positionierung durch Grosszuegigkeit** - Alle anderen wollen sofort Geld, Manuela gibt den besten Check kostenlos
2. **Die Fragen SIND die Beratung** - Wer 100 Fragen beantwortet, denkt 45 Min. ueber sein Business nach, sieht Luecken, wird "heiss"
3. **Upsell verkauft sich selbst** - Report zeigt WO Potenzial ist, aber nicht WIE man es hebt. Das WIE = Beratung/Kurs
4. **Unschlagbare Wahrnehmung** - "Wenn das KOSTENLOS ist, wie gut muss dann erst die Beratung sein?"

---

## 3. DIE 10 KATEGORIEN

| #  | Kategorie            | Prueft...                                    |
|----|----------------------|----------------------------------------------|
| 1  | Kommunikation        | E-Mails, Nachrichten, Korrespondenz          |
| 2  | Content-Erstellung   | Social Media, Blog, Newsletter, Website      |
| 3  | Kundengewinnung      | Marketing, Akquise, Angebote                 |
| 4  | Kundenbetreuung      | Support, Onboarding, Follow-up               |
| 5  | Wissensmanagement    | Recherche, Dokumentation, Lernen             |
| 6  | Administration       | Buchhaltung, Planung, Organisation           |
| 7  | Kreativprozesse      | Ideenfindung, Konzepte, Strategie            |
| 8  | Datennutzung         | Auswertungen, Reports, Entscheidungen        |
| 9  | Team & Fuehrung      | Delegation, Schulung, Zusammenarbeit         |
| 10 | KI-Readiness         | Mindset, Infrastruktur, Bereitschaft         |

**Wichtig:** Die Fragen muessen SO GUT sein, dass Leute nach Frage 20 denken "Wow, daran habe ich noch nie gedacht." Es sind MANUELAS Fragen - solche, die nur jemand stellen kann, der hunderte Unternehmen beraten hat.

---

## 4. TECHNISCHE ARCHITEKTUR

### Ziel-Stack (Vibe-Coding-Projekt):

```
Frontend:        Web-App mit Fragebogen (z.B. Next.js oder einfaches HTML/JS)
Scoring-Engine:  Automatische Auswertung pro Kategorie und Gesamt
Report-Generator: PDF-Erstellung mit personalisiertem Inhalt
E-Mail-Versand:  Automatische Zustellung des Reports
Backend:         Python/Node.js oder Serverless Functions
```

### Auswertungs-Report soll enthalten:
- **Gesamtscore** (z.B. 0-100 oder Prozent)
- **Score pro Kategorie** (10 Einzelwerte)
- **Visualisierung** (z.B. Spinnennetz-/Radar-Diagramm)
- **Staerken** (Top-3 Kategorien)
- **Luecken** (Bottom-3 Kategorien mit groesstem Hebel)
- **Top-3-Hebel** (konkrete Empfehlungen, was sofort umsetzbar ist)
- **Naechste Schritte** (mit CTA zu Manuelas Angeboten)

### Scoring-Logik (Konzept):
- Jede Frage hat eine Scoring-Dimension (z.B. 1-5 Skala oder Ja/Nein/Teilweise)
- Jede Kategorie hat vorformulierte Auswertungstexte in Abstufungen:
  - Score 0-30%: "Hier liegt enormes ungenutztes Potenzial..."
  - Score 31-60%: "Du hast erste Schritte gemacht, aber..."
  - Score 61-80%: "Gute Basis vorhanden, jetzt geht es um..."
  - Score 81-100%: "Beeindruckend! Du nutzt KI hier bereits stark..."
- System baut aus den Antworten einen individuellen Report zusammen

### Skalierung:
- Muss auf 10.000+ Nutzer skalieren ohne manuellen Aufwand
- Vollautomatisch von Fragebogen bis Report-Zustellung

---

## 5. OFFENE AUFGABEN / NAECHSTE SCHRITTE

### Phase 1: Fragen entwickeln
- [ ] 10 Fragen pro Kategorie formulieren (100 total)
- [ ] Fragen muessen praxisnah und augenoeffnend sein
- [ ] Scoring-Logik pro Frage definieren
- [ ] Fragetypen festlegen (Skala, Multiple Choice, Ja/Nein)

### Phase 2: Scoring & Auswertungstexte
- [ ] Scoring-Modell definieren (Gewichtung der Kategorien)
- [ ] Auswertungstexte pro Kategorie in 4 Abstufungen schreiben
- [ ] Top-3-Hebel-Logik: Welche Empfehlungen bei welchem Ergebnis?
- [ ] CTA-Texte formulieren (Uebergang zu Manuelas Angeboten)

### Phase 3: Technische Umsetzung
- [ ] Tech-Stack entscheiden (Web-Framework, Hosting)
- [ ] Frontend: Fragebogen-UI (responsiv, mobilfreundlich)
- [ ] Backend: Scoring-Engine implementieren
- [ ] PDF-Report-Generator bauen
- [ ] E-Mail-Integration (Report-Versand)
- [ ] Landing Page fuer den Check

### Phase 4: Launch
- [ ] Beta-Test mit 10-20 Personen
- [ ] Feedback einarbeiten
- [ ] Landing Page optimieren
- [ ] Launch-Strategie (Podcast, Social Media, Newsletter)

---

## 6. KONTEXT AUS DER BRAINSTORMING-SESSION

Die Idee des KI-Potenzial-Checks wurde in einer strukturierten Brainstorming-Session mit einem virtuellen Beraterstab entwickelt:

- **Herr Aydin (Strategieberater):** Vergleich mit erfolgreichen Freemium-Modellen (HubSpot, Calendly, Notion). Das kostenlose Tool ist die Eingangstuer, nicht das Produkt.
- **Frau Lindgren (Betriebswirtin):** Die 100 Fragen zwingen den Kunden, ueber sein Business nachzudenken. Danach WEISS er, dass er Hilfe braucht.
- **Herr Braun (Marketing):** Positionierung als "die Grosszuegige" - niemand sonst macht 100 Fragen kostenlos. Das IST die Marke.
- **Dr. Petrov (Technik):** Vollautomatische Auswertung ist ein realistisches Vibe-Coding-Projekt. Web-App mit Formular, Scoring-Logik und PDF-Generierung.
- **Frau Kessler (Psychologin):** Die Fragen selbst sind das Werkzeug - sie oeffnen Augen fuer blinde Flecken im Business.

### Weitere Ideen aus der Session (Parking Lot):
Neben dem 100-Fragen-Check wurden 8 weitere Ideen entwickelt (siehe `business-ideen-brainstorming.md`):
- Prompt-Bibliothek (digitales Produkt)
- "KI Quick Wins" Mini-Kurs
- Content-Recycling-Maschine fuer Podcast
- B2B KI-Strategie-Workshops
- Paid Community Membership
- Newsletter mit Affiliate-Einnahmen
- Lizenzmodell "KI Maestra fuer [Branche]"
- KI-Audit als Done-for-You Service

---

## 7. MANUELAS STIL UND TONALITAET

- Warm, nahbar, auf Augenhoehe
- Kein Tech-Jargon - Zielgruppe sind NICHT Techies
- Empowerment-Ansatz: "Du kannst das auch"
- Praxisorientiert: Immer konkrete Beispiele
- Sprache: Deutsch (DACH-Raum)
- Duzt ihre Community

---

## 8. WICHTIGE DATEIEN IN DIESEM REPO

- `business-ideen-brainstorming.md` - Alle 9 Business-Ideen im Detail
- `BRIEFING-KI-POTENZIAL-CHECK.md` - DIESES Dokument (Hauptbriefing)
- `app.py` / `main.py` - Bestehende Maestra-App (Meeting-Transkription)
- `requirements.txt` - Python-Dependencies

---

## 9. ANWEISUNGEN FUER CLAUDE CODE AM MACBOOK

Wenn Manuela dieses Briefing oeffnet und sagt "Lass uns weitermachen":

1. **Fragen zuerst** - Starte mit der Entwicklung der 100 Fragen. Arbeite Kategorie fuer Kategorie. Frage Manuela nach ihrer Expertise und ihren Erfahrungen, damit die Fragen authentisch und tiefgruendig werden.

2. **Interaktiv arbeiten** - Nicht einfach 100 Fragen generieren und abladen. Kategorie fuer Kategorie durchgehen, Manuelas Feedback einholen, iterieren.

3. **Vibe-Coding beachten** - Manuela coded mit Claude. Die technische Umsetzung soll als Vibe-Coding-Projekt machbar sein. Einfache, klare Architektur.

4. **Zielgruppe im Kopf behalten** - Jede Frage muss fuer eine Winzerin genauso verstaendlich sein wie fuer eine Business-Coach. Kein Fachjargon.

5. **Der Check muss WOW sein** - Das ist Manuelas Signature-Tool. Er muss so gut sein, dass Leute ihn weiterempfehlen. Qualitaet vor Geschwindigkeit.

---

*Dieses Briefing wurde am 2026-02-15 erstellt und fasst die komplette Brainstorming-Session zusammen.*
