import streamlit as st
import sys
import subprocess

st.title("AI Content Assistant")

st.write("Python version:", sys.version)

result = subprocess.run(
    [sys.executable, "-m", "pip", "show", "google-genai"],
    capture_output=True,
    text=True,
)

st.code(result.stdout or result.stderr)

try:
    from google import genai

    st.success("✅ google.genai imported successfully!")

except Exception as e:
    st.error(f"❌ Import failed: {e}")

    import google

    st.write("Google package location:")
    st.write(getattr(google, "__file__", "namespace package"))

    st.write("Google package path:")
    st.write(list(getattr(google, "__path__", [])))
