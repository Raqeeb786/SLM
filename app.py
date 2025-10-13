import streamlit as st
import pickle
import re
from retrieval import Retriever, search_docs
from slm_utils import clean_tokens

st.set_page_config(page_title="BharatSLM — Hindi Small Language Model", layout="centered")

@st.cache_resource
def load_models():
    models = {}
    for n in [2,3,4]:
        with open(f"models/{n}gram.pkl", "rb") as f:
            models[n] = pickle.load(f)
    return models

models = load_models()
retriever = Retriever("data")

def predict_top_words(tokens, top_k=3):
    for n in [4,3,2]:
        model = models[n]
        if len(tokens) < n-1:
            continue
        prefix = tuple(tokens[-(n-1):])
        next_words = model.ngrams_freq.get(prefix, {})
        #next_words = model["ngrams_freq"].get(prefix, {})
        if next_words:
            return [w for w, _ in next_words.most_common(top_k)]
    return []

def generate_text(context, mode="answer", max_words=30):
    tokens = clean_tokens(context.lower().split())
    for _ in range(max_words):
        top = predict_top_words(tokens)
        if not top: break
        next_word = top[0]
        tokens.append(next_word)
        if next_word in ["।", ".", "?", "!"]:
            break
    sentence = " ".join(tokens)
    sentence = re.split(r'[।.!?]', sentence)[0].strip()
    if mode == "question":
        if not sentence.endswith("?"): sentence += "?"
    else:
        if not sentence.endswith("।"): sentence += "।"
    return sentence

def generate_answer(user_q):
    results = search_docs(user_q, retriever, top_k=2)
    if not results: return "क्षमा करें, उत्तर उपलब्ध नहीं है।", 0.0
    texts, scores = zip(*results)
    confidence = sum(scores) / len(scores)
    context = " ".join(texts)[:500]
    combined = user_q + " " + context
    ans = generate_text(combined, mode="answer")
    return ans, confidence, results

# UI
st.title("🇮🇳 BharatSLM — 🔍 Hindi QA with Document Retrieval + n-gram Prediction")


user_q = st.text_input("📝 प्रश्न लिखें:")
if user_q.strip():
    ans, conf, docs = generate_answer(user_q)
    st.success(ans)
    st.write(f"🔎 विश्वास स्तर: {conf:.2f}")
    st.markdown("📄 **शीर्ष दस्तावेज़:**")
    for i, (doc, sc) in enumerate(docs, 1):
        st.markdown(f"**{i}.** {doc[:150]}... *(स्कोर: {sc:.3f})*")

