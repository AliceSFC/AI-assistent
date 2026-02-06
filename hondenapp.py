import streamlit as st

# Titel
st.title("🐕 Hondenleeftijd Calculator")

# Tekst
st.write("Bereken de leeftijd van je hond in mensenjaren!")

# Input voor hondennaam
hond_naam = st.text_input("Wat is de naam van je hond?", "Buddy")

# Slider voor leeftijd
hond_leeftijd = st.slider("Hoe oud is je hond?", 0, 20)

# Berekening (moderne methode)
if hond_leeftijd == 0:
    mensen_leeftijd = 0
elif hond_leeftijd == 1:
    mensen_leeftijd = 15
elif hond_leeftijd == 2:
    mensen_leeftijd = 24
else:
    mensen_leeftijd = 24 + (hond_leeftijd - 2) * 4

# Resultaat tonen
st.write(f"### {hond_naam} is ongeveer **{mensen_leeftijd} mensenjaren** oud!")

# Extra info
if mensen_leeftijd < 18:
    st.info(f"🐶 {hond_naam} is nog een puppy of tiener!")
elif mensen_leeftijd < 60:
    st.success(f"💪 {hond_naam} is in de bloei van zijn/haar leven!")
else:
    st.warning(f"👴 {hond_naam} is een senior hond. Geef extra zorg!")