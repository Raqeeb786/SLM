# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# class Retriever:
#     def __init__(self, data_dir):
#         self.documents = []
#         for file in os.listdir(data_dir):
#             if file.endswith(".txt"):
#                 with open(os.path.join(data_dir, file), encoding="utf-8") as f:
#                     self.documents.append(f.read())
#         self.vectorizer = TfidfVectorizer()
#         self.doc_vectors = self.vectorizer.fit_transform(self.documents)

# def search_docs(query, retriever, top_k=2):
#     query_vec = retriever.vectorizer.transform([query])
#     sims = cosine_similarity(query_vec, retriever.doc_vectors)[0]
#     top_indices = sims.argsort()[-top_k:][::-1]
#     return [(retriever.documents[i], sims[i]) for i in top_indices]





import os, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def hindi_tokenizer(text):
    text = re.sub(r'[^\u0900-\u097F\s]', '', text)
    return text.split()

def load_documents(data_dir):
    docs = []
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):
            with open(os.path.join(data_dir, file), encoding="utf-8") as f:
                text = f.read()
                sentences = re.split(r'[।.!?]', text)
                docs.extend([s.strip() for s in sentences if len(s.strip()) > 5])
    return docs

class Retriever:
    def __init__(self, data_dir):
        self.documents = load_documents(data_dir)
        self.vectorizer = TfidfVectorizer(tokenizer=hindi_tokenizer, lowercase=True)
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

def search_docs(query, retriever, top_k=3):
    query_vec = retriever.vectorizer.transform([query])
    sims = cosine_similarity(query_vec, retriever.doc_vectors)[0]
    top_indices = sims.argsort()[-top_k:][::-1]
    return [(retriever.documents[i], sims[i]) for i in top_indices]
