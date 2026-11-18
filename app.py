import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Prompt Injection Detector",
    page_icon="🛡️"
)

MODEL_DIR = Path(__file__).parent / "saved_models"

@st.cache_resource
def load_models():
    vectorizer = joblib.load(
        MODEL_DIR / "tfidf_vectorizer.joblib"
    )
    lr = joblib.load(
        MODEL_DIR / "logistic_regression.joblib"
    )
    svm = joblib.load(
        MODEL_DIR / "linear_svm.joblib"
    )
    return vectorizer, lr, svm

st.title("🛡️ Prompt Injection Detector")

st.write(
    "Machine learning-based detection of potential "
    "direct prompt injection attempts in LLM inputs."
)

vectorizer, lr_model, svm_model = load_models()

model_choice = st.selectbox(
    "Select classification model",
    ["Logistic Regression", "Linear SVM"]
)

prompt = st.text_area(
    "Enter text to analyze",
    placeholder="Enter a user prompt...",
    height=160,
    max_chars=10000
)

if st.button("Analyze Prompt", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        model = (
            lr_model
            if model_choice == "Logistic Regression"
            else svm_model
        )

        features = vectorizer.transform([prompt])
        prediction = int(model.predict(features)[0])

        if prediction == 1:
            st.error("Potential Prompt Injection Detected")
            st.write(
                "This input was flagged as potentially malicious. "
                "Additional review may be needed."
            )
        else:
            st.success("No Prompt Injection Detected")
            st.write(
                "The model classified this input as benign. "
                "This does not guarantee that it is safe."
            )

st.divider()

st.caption(
    "Research prototype for CYBERSEC 520. "
    "The models may miss unfamiliar attacks or flag "
    "legitimate prompts. Predictions should not replace "
    "authorization controls or human review."
)
