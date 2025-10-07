import streamlit as st
import pickle
from slm_utils import clean_tokens

# Must be first
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

# Predict top 3 words using backoff from 4→3→2-gram
def predict_top_words(context, top_k=3):
    for n in [4, 3, 2]:
        model = models[n]
        tokens = clean_tokens(context.lower().split())
        prefix = tuple(tokens[-(n - 1):])
        possible_words = model.ngrams_freq.get(prefix, {})
        if possible_words:
            return [w for w, _ in possible_words.most_common(top_k)]
    return []

def predict_full_sentence(context, max_words=10):
    words = clean_tokens(context.lower().split())
    for _ in range(max_words):
        top = predict_top_words(" ".join(words), top_k=1)
        if not top or top[0] in ("</s>", "<कोई सुझाव नहीं>"):
            break
        words.append(top[0])
    return " ".join(words)

# Title & Instructions
st.title("🔤 Hindi Sentence Auto-Completor")
st.markdown("Start typing a Hindi sentence. Suggestions will appear live below.")

# Session state to preserve user input across clicks
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# User text input (bind to session state)
user_text = st.text_input("📝 Type here:", value=st.session_state.user_input, max_chars=200)

# Update session state if input changes
if user_text != st.session_state.user_input:
    st.session_state.user_input = user_text

# Predict if input is non-empty
if user_text.strip():
    suggestions = predict_top_words(user_text, top_k=3)
    full_sentence = predict_full_sentence(user_text)

    st.markdown("### 🔮 Suggestions:")

    # Show top 3 suggestions as buttons
    cols = st.columns(len(suggestions))
    for i, word in enumerate(suggestions):
        if cols[i].button(word):
            # Append selected suggestion to input
            st.session_state.user_input += " " + word
            st.rerun()

    st.markdown("### 🧠 Completed Sentence:")
    st.success(full_sentence)
else:
    st.warning("👆 Start typing above to see suggestions.")
