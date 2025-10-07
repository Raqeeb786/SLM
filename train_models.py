import pickle
from slm_utils import NGramModel, clean_corpus

# Load raw corpus
with open('hindi_corpus_sample_cleaned.txt', 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

# Clean the corpus
cleaned_lines = clean_corpus(raw_lines)
joined_corpus = " ".join(cleaned_lines)

# Train models
models = {
    2: NGramModel(2),
    3: NGramModel(3),
    4: NGramModel(4),
}

for n, model in models.items():
    print(f"Training {n}-gram model...")
    model.train(joined_corpus)

    # Save model
    with open(f"models/{n}gram.pkl", "wb") as f:
        pickle.dump(model, f)

print("✅ All models trained and saved.")




