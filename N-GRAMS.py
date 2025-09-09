import nltk
from nltk.util import ngrams
from collections import defaultdict, Counter
import random
import pandas as pd

nltk.download('punkt')

import string

def clean_tokens(tokens):
    return [t.strip(string.punctuation) for t in tokens if t.strip()]

class NGramModel:
    def __init__(self, n):
        self.n = n
        self.ngrams_freq = defaultdict(Counter)

    # def train(self, text_corpus):
    #     #tokens = nltk.word_tokenize(text_corpus.lower())
    #     tokens = text_corpus.lower().split()
    #     for gram in ngrams(tokens, self.n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
    #         prefix = gram[:-1]
    #         next_word = gram[-1]
    #         self.ngrams_freq[prefix][next_word] += 1

    def train(self, text_corpus):
        tokens = clean_tokens(text_corpus.lower().split())
        for gram in ngrams(tokens, self.n, pad_left=True, pad_right=True,
                        left_pad_symbol='<s>', right_pad_symbol='</s>'):
            prefix = gram[:-1]
            next_word = gram[-1]
            self.ngrams_freq[prefix][next_word] += 1

    # def predict_next(self, context):
    #     context = tuple(context.lower().split()[-(self.n - 1):])
    #     possible_words = self.ngrams_freq.get(context, {})
    #     if not possible_words:
    #         return "<no prediction>"
    #     return possible_words.most_common(1)[0][0]
    
    def predict_next(self, context):
        tokens = clean_tokens(context.lower().split())
        context = tuple(tokens[-(self.n - 1):])
        possible_words = self.ngrams_freq.get(context, {})
        if not possible_words:
            return "<no prediction>"
        return possible_words.most_common(1)[0][0]


# Load your captions
with open('final_captions.txt','r',encoding='utf-8')as f:
    corpus= f.readlines()

# Train the model
model = NGramModel(n=3)  # Trigram model
#model.train(corpus)
model.train(" ".join(corpus))


# Example predictions
while True:
    user_input = input("Enter a phrase: ")
    if user_input.lower() == 'exit':
        break
    next_word = model.predict_next(user_input)
    print(f"→ Predicted next word: {next_word}")