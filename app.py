import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="SQL Query Explainer", page_icon="🔍")

st.title("🔍 SQL Query Explainer")
st.write("Paste any SQL query and get a plain-English explanation.")

query_input = st.text_area(
    "Paste your SQL query here:",
    height=200,
    placeholder="SELECT * FROM employees WHERE salary > 50000;"
)

if st.button("Explain Query"):
    if query_input.strip() == "":
        st.warning("Please paste a SQL query first.")
    else:
        with st.spinner("Analyzing your query..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert SQL tutor. 
                        Explain SQL queries in simple, clear English.
                        Structure your response as:
                        1. What it does (1 sentence)
                        2. Step by step breakdown
                        3. One real-world use case
                        Keep it concise — under 150 words total."""
                    },
                    {
                        "role": "user",
                        "content": f"Explain this SQL query:\n\n{query_input}"
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            explanation = response.choices[0].message.content
        
        st.success("Explanation:")
        st.markdown(explanation)

st.divider()
st.caption("Built using OpenAI GPT-3.5 + Streamlit | by Manideep")