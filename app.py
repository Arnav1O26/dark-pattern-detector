import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import process_input
from detector import analyze_snippets

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Dark Pattern Detector",
    page_icon="🕵️",
    layout="wide"
)

# ==========================================
# SIDEBAR: DOCUMENTATION & EXAMPLES
# ==========================================
with st.sidebar:
    st.header("How It Works")
    st.write("This tool extracts short UI text from a webpage and analyzes it for manipulative design patterns.")
    
    st.subheader("Scoring Formula")
    st.info(
        "**Manipulation Score (0-100):**\n\n"
        "Each flagged snippet adds up to 20 points to the total score, weighted by the model's confidence. "
        "The final score is capped at 100."
    )
    
    st.subheader("Pattern Glossary")
    st.markdown("""
    *   **False Urgency:** Manufactured deadlines to rush decisions. *(e.g., "Offer ends in 02:14")*
    *   **Social Proof Pressure:** Using group behavior to pressure users. *(e.g., "15 people are looking at this")*
    *   **Forced Continuity:** Making subscriptions easy to join but hard to leave. *(e.g., "Card will be charged automatically")*
    *   **Confirmshaming:** Guilt-tripping the user for opting out. *(e.g., "No thanks, I hate saving money")*
    *   **Hidden Costs:** Undisclosed fees added at the very end. *(e.g., "Service fee applied")*
    """)

# ==========================================
# MAIN UI: INPUT & ANALYSIS
# ==========================================
st.title("🕵️ Dark Pattern Detector")
st.write("Expose manipulative e-commerce tactics using Regex and Machine Learning.")

# User Input Section
input_type = st.radio("Select Input Method:", ("URL", "Raw HTML/Text"), horizontal=True)

if input_type == "URL":
    user_input = st.text_input("Enter Webpage URL:", placeholder="https://example.com")
    is_url = True
else:
    user_input = st.text_area("Paste HTML or Text:", height=200, placeholder="Paste page source or UI text here...")
    is_url = False

if st.button("Analyze for Dark Patterns", type="primary"):
    if not user_input.strip():
        st.warning("Please provide an input to analyze.")
    else:
        with st.spinner("Extracting and analyzing UI snippets..."):
            
            # Step 1: Scrape
            snippets, error = process_input(user_input, is_url=is_url)
            
            if error:
                st.error(error)
            elif not snippets:
                st.warning("No valid UI text snippets found. Try pasting the raw HTML instead.")
            else:
                # Step 2: Analyze
                score, results = analyze_snippets(snippets)
                
                st.divider()
                
                # ==========================================
                # RESULTS DASHBOARD
                # ==========================================
                
                # 1. Top Level Metric
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(label="Manipulation Score", value=f"{score} / 100")
                    if score < 20:
                        st.success("Low Risk: Few to no patterns detected.")
                    elif score < 60:
                        st.warning("Medium Risk: Several manipulative patterns found.")
                    else:
                        st.error("High Risk: Highly manipulative UI detected.")
                
                with col2:
                    # Simple visual progress bar for the score
                    st.progress(int(score))
                
                st.write(f"*Analyzed {len(snippets)} UI snippets.*")
                
                if results:
                    # Convert results to a Pandas DataFrame for easy sorting and charting
                    df = pd.DataFrame(results)
                    
                    st.subheader("Detected Dark Patterns")
                    
                    # 2. Plotly Bar Chart
                    # Group by category to see the breakdown
                    category_counts = df['Category'].value_counts().reset_index()
                    category_counts.columns = ['Category', 'Count']
                    
                    fig = px.bar(
                        category_counts, 
                        x='Count', 
                        y='Category', 
                        orientation='h',
                        title="Dark Patterns Breakdown",
                        color='Category'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 3. Sortable Data Table
                    st.write("### Detailed Breakdown")
                    st.dataframe(
                        df, 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                            "Confidence (%)": st.column_config.ProgressColumn(
                                "Confidence (%)", min_value=0, max_value=100
                            )
                        }
                    )
                else:
                    st.success("🎉 No dark patterns detected in the analyzed snippets!")