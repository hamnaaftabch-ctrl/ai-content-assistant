import streamlit as st

st.title("AI Content Assistant")

try:
    from google import genai

    st.success("Google GenAI SDK imported successfully!")

except Exception as e:
    st.error(f"Import failed: {e}")
