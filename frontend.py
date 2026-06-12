import streamlit as st
from main import get_data_from_database

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon = "🤖",
    layout = "centered"
)

st.title("🤖 AI Data Analyst")
st.markdown("Ask question about your data in natural language")

user_query = st.text_area("Enter your question : " , placeholder="e.g. Compare total clicks and applications for October 2025")

if st.button("Analyze"):
    if user_query.strip() == "":
        st.warning("Please Enter a valid question")
    else:
        with st.spinner("Analyzing your query..."):
            database_response = get_data_from_database(user_query)
            fixed_answer = f"🔍 Heres the analysis of your query\n\n**{user_query}**\n\{database_response}"
        st.success("Analysis Complete")
        st.markdown(fixed_answer)