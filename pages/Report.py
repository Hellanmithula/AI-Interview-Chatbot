import streamlit as st

st.set_page_config(page_title="Report", layout="centered")

st.title("📊 Interview Report")

if "feedback_history" not in st.session_state or len(st.session_state.feedback_history) == 0:
    st.warning("No interview data found. Please complete the interview first.")
else:
    for i, item in enumerate(st.session_state.feedback_history):
        st.markdown(f"## Question {i+1}")
        st.write("**Question:**", item["question"])
        st.write("**Your Answer:**", item["answer"])

        st.markdown("### 💡 Feedback")
        st.write(item["feedback"])

        st.markdown("---")