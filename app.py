"""CYBERSEC 520: direct prompt-injection screening demo.

The saved Logistic Regression classifier checks each submitted message before
this demo sends it to Gemini. This is a research prototype, not a production
security control.
"""

from pathlib import Path

import joblib
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Screened AI Assistant",
    page_icon="💬",
    layout="centered",
)

MODEL_DIR = Path(__file__).parent / "saved_models"
# Use the same Flash-Lite model that worked in your local test.
GEMINI_MODEL = "gemini-3.1-flash-lite"


@st.cache_resource
def load_detector():
    """Load the training-time TF-IDF vectorizer and trained LR classifier."""
    vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.joblib")
    classifier = joblib.load(MODEL_DIR / "logistic_regression.joblib")
    return vectorizer, classifier


st.title("Ask the assistant")
st.write(
    "This demo checks your message for potential prompt injection "
    "before sending it to Gemini."
)
st.caption("Research demonstration · Use fictional or non-sensitive questions only.")

try:
    vectorizer, classifier = load_detector()
except Exception:
    st.error("The screening model could not be loaded. Check the saved_models folder.")
    st.stop()

with st.form("message_form", clear_on_submit=False):
    prompt = st.text_area(
        "Your message",
        placeholder="What would you like to ask?",
        height=140,
        max_chars=10000,
    )
    submitted = st.form_submit_button("Send message", type="primary", use_container_width=True)

if submitted:
    message = prompt.strip()

    if not message:
        st.warning("Please enter a message first.")
    else:
        try:
            features = vectorizer.transform([message])
            prediction = int(classifier.predict(features)[0])
        except Exception:
            st.error("The screening step failed. Your message was not sent to Gemini.")
            st.stop()

        if prediction == 1:
            st.warning("Potential Prompt Injection Detected")
            st.write(
                "The screening model flagged this message as a possible prompt "
                "injection attempt, so it was not forwarded to Gemini."
            )
            st.caption(
                "Automated screening can make mistakes. A flagged message is "
                "not proof of malicious intent."
            )
        elif prediction == 0:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except (FileNotFoundError, KeyError):
                st.error(
                    "The message passed screening, but Gemini is not configured. "
                    "Add GEMINI_API_KEY to .streamlit/secrets.toml."
                )
            else:
                try:
                    with st.spinner("Getting a response..."):
                        client = genai.Client(api_key=api_key)
                        response = client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=message,
                        )

                    st.success("Message passed screening and was sent to Gemini")
                    st.subheader("Assistant response")
                    st.write(response.text or "Gemini did not return a text response.")
                except Exception as exc:
                    code = getattr(exc, "code", None)
                    st.error(
                        "The message passed screening, but Gemini could not respond. "
                        "Check your API settings or usage limits."
                        + (f" (API error {code})" if code is not None else "")
                    )
        else:
            st.error("Unexpected model output. Your message was not forwarded.")


st.divider()
st.caption(
    "CYBERSEC 520 research prototype. Classification is imperfect: suspicious "
    "inputs may be missed and legitimate messages may be flagged. This demo "
    "does not replace authorization, tool permissions, logging, or human review."
)
