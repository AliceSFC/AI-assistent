import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

st.title("📚 Huiswerk & Toetsen Planner")
st.write("Plan je huiswerk, toetsen en projecten!")

# Voorbeeldgegevens voor de kalender
calendar_events = [
    {
        "title": "Wiskundetoets",
        "start": "2026-02-05",
        "end": "2026-02-05",
        "backgroundColor": "#FF6B6B",
    },
    {
        "title": "Werkstuk Nederlands inleveren",
        "start": "2026-02-10",
        "end": "2026-02-10",
        "backgroundColor": "#4ECDC4",
    },
    {
        "title": "Geschiedenispresentatie",
        "start": "2026-02-15",
        "end": "2026-02-15",
        "backgroundColor": "#FFE66D",
    },
    {
        "title": "Biologie practicum",
        "start": "2026-02-20",
        "end": "2026-02-20",
        "backgroundColor": "#95E1D3",
    }
]

# Kalender opties
calendar_options = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth",
    "selectable": True,
}

# Toon de kalender
selected_event = calendar(events=calendar_events, options=calendar_options)

# Formulier om nieuwe events toe te voegen
st.subheader("➕ Voeg een nieuwe taak toe")

col1, col2 = st.columns(2)

with col1:
    taak_naam = st.text_input("Taak naam", "Huiswerk maken")
    taak_datum = st.date_input("Datum", datetime.now())

with col2:
    taak_type = st.selectbox("Type", ["Toets", "Huiswerk", "Project", "Presentatie"])
    
    # Kleur kiezen op basis van type
    kleuren = {
        "Toets": "#FF6B6B",
        "Huiswerk": "#4ECDC4",
        "Project": "#FFE66D",
        "Presentatie": "#95E1D3"
    }

if st.button("Taak toevoegen"):
    st.success(f"✅ '{taak_naam}' toegevoegd voor {taak_datum}!")
    st.info("💡 Tip: In een echte app zou dit opgeslagen worden in een database")

# Toon geselecteerd event
if selected_event:
    st.write("### Geselecteerde taak:")
    st.json(selected_event)