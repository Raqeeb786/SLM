
````markdown
# Hindi N-gram Next Word Predictor

A simple next-word predictor (autocomplete) built using n-gram language models trained on a sampled Hindi corpus from the AI4Bharat IndicCorp dataset.  
No heavy deep learning or transfer learning — lightweight and interpretable.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Dataset](#dataset)  
- [Setup](#setup)  
- [Corpus Preparation](#corpus-preparation)  
- [Training the N-gram Models](#training-the-n-gram-models)  
- [Usage](#usage)  
- [Future Improvements](#future-improvements)  
- [References](#references)  

---

## Project Overview

This project implements a simple n-gram language model (bigram, trigram, 4-gram) for Hindi language next-word prediction using:

- A cleaned and sampled Hindi text corpus (~200k sentences) from AI4Bharat IndicCorp dataset  
- Basic text preprocessing and cleaning  
- Python and NLTK for tokenization and n-gram extraction  

---

## Dataset

**AI4Bharat IndicCorpV2**

- A large-scale multilingual Indic language corpus, publicly available on Hugging Face Datasets.  
- Link: https://huggingface.co/datasets/ai4bharat/IndicCorpV2  
- The full Hindi dataset is around 16 GB in size, so this project streams and samples a smaller subset (~200,000 lines) for efficient training.  

---

## Setup

### Requirements

- Python 3.7 or above  
- Install required libraries:  
  ```bash
  pip install datasets nltk

- Download NLTK tokenizer data (run once):

  ```python
  import nltk
  nltk.download('punkt')
  ```

---

## Corpus Preparation

Run the `prepare_corpus.py` script to download, sample, clean, and save the Hindi corpus:

```bash
python prepare_corpus.py
```

This script will:

* Stream the Hindi split of IndicCorp dataset (no need to download the full 16GB)
* Randomly sample 200,000 sentences (adjustable in the script)
* Clean sentences by removing unwanted characters, normalizing whitespace
* Remove duplicate sentences for a cleaner dataset
* Save the cleaned corpus as `hindi_corpus_sample_cleaned.txt`

---

## Training the N-gram Models

Use your existing n-gram training script (`train_models.py`) or code to train models on the cleaned corpus:

```python
with open('hindi_corpus_sample_cleaned.txt', 'r', encoding='utf-8') as f:
    corpus = f.read()

model = NGramModel(n=3)  # Train trigram model as example
model.train(corpus)

print(model.predict_next("मैं आज"))  # Example prediction
```

You can similarly train bigram, trigram, and 4-gram models by changing the `n` parameter.

---

## Usage

Use the trained model to predict the next word for any Hindi phrase:

```python
context = "तुम कैसे"
next_word = model.predict_next(context)
print(f"Next word prediction: {next_word}")
```

---

## Future Improvements

* Add **smoothing techniques** (e.g., Laplace smoothing) to better handle unseen n-grams
* Combine multiple small Hindi corpora to improve diversity and domain adaptation
* Extend the model to predict full phrase completions instead of just the next word
* Build a web interface (e.g., Streamlit app) for interactive autocomplete
* Explore lightweight embedding or neural methods if you want better accuracy without heavy models

---

## References

* [AI4Bharat IndicCorp Dataset on Hugging Face](https://huggingface.co/datasets/ai4bharat/IndicCorpV2)
* [NLTK Documentation](https://www.nltk.org/)
* [Hugging Face Datasets Documentation](https://huggingface.co/docs/datasets/)

---

*This project is intended as a lightweight and interpretable solution for next-word prediction in Hindi without relying on deep learning models or large pretrained language models.*

```

---