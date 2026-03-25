import streamlit as st
import random
from PyPDF2 import PdfReader
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3

st.set_page_config(page_title="AI INTERVIEW CHATBOT", layout="centered")

# ---------- UI ----------
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
</style>
""", unsafe_allow_html=True)

# ---------- WHISPER ----------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

# ---------- SPEAK ----------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------- AUDIO ----------
def record_audio():
    fs = 44100
    duration = 12

    if st.button("🎤 Record Answer"):
        st.warning("Recording... Speak now")

        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        write("audio.wav", fs, recording)

        model = load_model()
        result = model.transcribe("audio.wav")

        text = result["text"]
        st.success(f"🗣️ {text}")

        return text

    return None

# ---------- RESUME ----------
def read_resume(file):
    text = ""
    reader = PdfReader(file)
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t
    return text.lower()

# ---------- QUESTIONS ----------
def generate_question(text):
    questions = []

    if "python" in text:
        questions += [
            "Explain a Python project you built",
            "What libraries have you used in Python?",
            "What is list comprehension in Python?"
        ]

    if "machine learning" in text:
        questions += [
            "Explain a machine learning project",
            "What is overfitting?",
            "What algorithms have you used?"
        ]

    questions += [
        "Tell me about yourself",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?"
    ]

    if "asked_questions" not in st.session_state:
        st.session_state.asked_questions = []

    remaining = list(set(questions) - set(st.session_state.asked_questions))

    if not remaining:
        st.session_state.asked_questions = []
        remaining = questions

    q = random.choice(remaining)
    st.session_state.asked_questions.append(q)

    return q

# ---------- SMART FEEDBACK ----------
def get_ai_feedback(question, answer):
    feedback = []
    words = answer.split()

    if len(words) < 20:
        feedback.append("⚠️ Your answer is too short. Try explaining more clearly.")
    elif len(words) > 80:
        feedback.append("⚠️ Your answer is too long. Try to be concise.")
    else:
        feedback.append("✅ Good answer length.")

    if "project" in answer.lower():
        feedback.append("✅ Good: You included practical experience.")
    else:
        feedback.append("⚠️ Add a real project or example.")

    weak_words = ["i think", "maybe", "not sure"]
    if any(w in answer.lower() for w in weak_words):
        feedback.append("⚠️ Avoid weak phrases. Speak confidently.")
    else:
        feedback.append("✅ Your tone sounds confident.")

    feedback.append(f"\n💡 Tip for this question: '{question}'")

    if "yourself" in question.lower():
        feedback.append("👉 Include background, skills, and goals.")
    elif "strength" in question.lower():
        feedback.append("👉 Mention strengths with examples.")
    elif "weakness" in question.lower():
        feedback.append("👉 Be honest and show improvement.")
    elif "project" in question.lower():
        feedback.append("👉 Explain problem, solution, and result.")

    feedback.append("\n🧠 Better Answer Example:")
    feedback.append(
        "I worked on a project where I applied my skills to solve a real problem. "
        "I focused on delivering efficient results and gained valuable experience."
    )

    return "\n".join(feedback)

# ---------- SESSION ----------
if "resume" not in st.session_state:
    st.session_state.resume = ""
if "q" not in st.session_state:
    st.session_state.q = ""
if "name" not in st.session_state:
    st.session_state.name = ""
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []

# ---------- UI ----------
st.title("🤖 AI INTERVIEW CHATBOT")

name = st.text_input("Enter your name")

if name:
    st.session_state.name = name

resume = st.file_uploader("📄 Upload Resume", type=["pdf"])

if resume:
    st.session_state.resume = read_resume(resume)
    st.success("Resume loaded")

# START
if st.button("▶️ Start Interview"):
    st.session_state.q = generate_question(st.session_state.resume)

    if name:
        speak(f"Hello {name}, let's begin your interview")
    else:
        speak("Hello, let's begin your interview")

# FLOW
if st.session_state.q:
    st.subheader(st.session_state.q)

    if st.button("🔊 Hear Question"):
        speak(st.session_state.q)

    answer = record_audio()

    if answer:
        st.info("🧠 Analyzing your answer...")

        feedback = get_ai_feedback(st.session_state.q, answer)

        st.markdown("### 💡 Interview Feedback")
        st.write(feedback)

        # Save history
        st.session_state.feedback_history.append({
            "question": st.session_state.q,
            "answer": answer,
            "feedback": feedback
        })

        speak("Here is your feedback")

        for line in feedback.split("\n"):
            if line.strip():
                speak(line)

        # Next question
        st.session_state.q = generate_question(st.session_state.resume)

        speak("Next question")
        speak(st.session_state.q)

        st.rerun()

# REPORT BUTTON
if st.button("📊 View Report"):
    st.switch_page("pages/Report.py")