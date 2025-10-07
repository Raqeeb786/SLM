import streamlit as st
import pickle
from slm_utils import clean_tokens

# ✅ Must be first
st.set_page_config(page_title="Hindi Auto-Completion", layout="centered")

# Load N-gram models
@st.cache_resource
def load_models():
    models = {}
    for n in [2, 3, 4]:
        with open(f"models/{n}gram.pkl", "rb") as f:
            models[n] = pickle.load(f)
    return models

models = load_models()

# Predict using backoff from 4→3→2-gram
def predict_next_word(context):
    for n in [4, 3, 2]:
        model = models[n]
        prediction = model.predict_next(context)
        if prediction and prediction != "<no prediction>":
            return prediction
    return "<कोई सुझाव नहीं>"

def predict_full_sentence(context, max_words=10):
    words = clean_tokens(context.lower().split())
    for _ in range(max_words):
        next_word = predict_next_word(" ".join(words))
        if next_word in ("</s>", "<कोई सुझाव नहीं>"):
            break
        words.append(next_word)
    return " ".join(words)

# UI
st.title("🔤 Hindi Sentence Auto-Completor")
st.markdown("Start typing a Hindi sentence — predictions will update automatically.")

# Live prediction
user_input = st.text_input("📝 Type here:", max_chars=200)

if user_input.strip():
    next_word = predict_next_word(user_input)
    full_sentence = predict_full_sentence(user_input)
    
    st.markdown("### 🔮 Predictions:")
    st.info(f"**Next Word:** {next_word}")
    st.success(f"**Completed Sentence:** {full_sentence}")
else:
    st.warning("👆 Start typing above to see predictions.")
