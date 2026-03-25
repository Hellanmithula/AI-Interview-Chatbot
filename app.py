import streamlit as st

st.set_page_config(page_title="AI INTERVIEW CHATBOT", layout="centered")

# UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}
h1 {
    text-align: center;
    color: #00f5ff;
}
.stButton>button {
    background: linear-gradient(90deg, #00f5ff, #00c6ff);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI INTERVIEW CHATBOT")
st.markdown("### 🚀 Practice Like a Real Interview")

st.write("""
👉 Use the sidebar to navigate:
- 🎤 Interview
- 📊 Report
""")