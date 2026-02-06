import streamlit as st
import cohere
import os

# Configuratie van de pagina
st.set_page_config(
    page_title="Tekst Samenvatting Tool",
    page_icon="📝",
    layout="wide"
)

# Titel en beschrijving
st.title("📝 Tekst Samenvatting Tool")
st.markdown("Vat grote hoeveelheden tekst samen met Cohere AI")

# Sidebar voor API key en instellingen
with st.sidebar:
    st.header("⚙️ Instellingen")
    
    # API Key invoer
    api_key = st.text_input(
        "Cohere API Key",
        type="password",
        help="Verkrijg je API key op cohere.com"
    )
    
    st.markdown("---")
    
    # Samenvattingsopties
    st.subheader("Samenvattingsopties")
    
    length = st.select_slider(
        "Lengte van samenvatting",
        options=["short", "medium", "long"],
        value="medium",
        help="Hoe lang moet de samenvatting zijn?"
    )
    
    format_type = st.selectbox(
        "Formaat",
        ["paragraph", "bullets"],
        help="Alinea of bullet points"
    )
    
    extractiveness = st.select_slider(
        "Extractiviteit",
        options=["low", "medium", "high"],
        value="medium",
        help="Low = meer herschrijven, High = meer citaten uit originele tekst"
    )
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips
    - Voor beste resultaten: gebruik duidelijke, gestructureerde tekst
    - Maximum tekst lengte: ~50.000 karakters
    - Voor zeer lange documenten wordt de tekst automatisch opgesplitst
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Invoer Tekst")
    
    # Tekst invoer opties
    input_method = st.radio(
        "Hoe wil je tekst invoeren?",
        ["Plak tekst", "Upload bestand"],
        horizontal=True
    )
    
    text_to_summarize = ""
    
    if input_method == "Plak tekst":
        text_to_summarize = st.text_area(
            "Plak hier je tekst:",
            height=400,
            placeholder="Voer of plak hier de tekst die je wilt samenvatten..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload een tekstbestand",
            type=["txt", "md"],
            help="Ondersteunde formaten: .txt, .md"
        )
        
        if uploaded_file is not None:
            text_to_summarize = uploaded_file.read().decode("utf-8")
            st.text_area(
                "Geüploade tekst:",
                value=text_to_summarize,
                height=400,
                disabled=True
            )
    
    # Toon statistieken van de invoer
    if text_to_summarize:
        word_count = len(text_to_summarize.split())
        char_count = len(text_to_summarize)
        st.info(f"📊 Statistieken: {word_count} woorden, {char_count} karakters")

with col2:
    st.subheader("✨ Samenvatting")
    
    # Placeholder voor samenvatting
    summary_placeholder = st.empty()
    
    # Samenvat knop
    if st.button("🚀 Genereer Samenvatting", type="primary", use_container_width=True):
        
        # Validatie
        if not api_key:
            st.error("⚠️ Voer eerst je Cohere API key in de sidebar in!")
        elif not text_to_summarize:
            st.error("⚠️ Voer eerst tekst in om samen te vatten!")
        elif len(text_to_summarize.strip()) < 250:
            st.warning("⚠️ De tekst is te kort om goed samen te vatten. Voer minimaal 250 karakters in.")
        else:
            try:
                # Initialiseer Cohere client
                co = cohere.Client(api_key)
                
                # Progress indicator
                with st.spinner("🤖 Bezig met samenvatten..."):
                    
                    # Check of tekst te lang is (max ~50k karakters voor Cohere)
                    max_chars = 50000
                    
                    if len(text_to_summarize) > max_chars:
                        st.warning(f"⚠️ Tekst is langer dan {max_chars} karakters. Eerste {max_chars} karakters worden gebruikt.")
                        text_to_summarize = text_to_summarize[:max_chars]
                    
                    # Roep Cohere summarize endpoint aan
                    response = co.summarize(
                        text=text_to_summarize,
                        length=length,
                        format=format_type,
                        extractiveness=extractiveness,
                        temperature=0.3
                    )
                    
                    summary = response.summary
                    
                    # Toon samenvatting
                    with summary_placeholder.container():
                        st.markdown("### 📋 Resultaat")
                        st.write(summary)
                        
                        # Statistieken van samenvatting
                        summary_word_count = len(summary.split())
                        summary_char_count = len(summary)
                        original_word_count = len(text_to_summarize.split())
                        
                        compression_ratio = round((1 - summary_word_count / original_word_count) * 100, 1)
                        
                        st.success(f"""
                        ✅ Samenvatting gegenereerd!  
                        📊 {summary_word_count} woorden ({summary_char_count} karakters)  
                        📉 {compression_ratio}% compressie
                        """)
                        
                        # Download knop
                        st.download_button(
                            label="💾 Download Samenvatting",
                            data=summary,
                            file_name="samenvatting.txt",
                            mime="text/plain"
                        )
                
            except Exception as e:
                st.error(f"❌ Er is een fout opgetreden: {str(e)}")
                st.info("💡 Controleer of je API key correct is en of je internetverbinding werkt.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Gemaakt met Streamlit en Cohere API | 
    <a href='https://cohere.com' target='_blank'>Verkrijg je API key</a>
</div>
""", unsafe_allow_html=True)