import re
import string
import random
from collections import defaultdict, Counter
from nltk.util import ngrams
import nltk

nltk.download('punkt')

# Clean a list of lines
def clean_corpus(corpus_lines):
    cleaned = []
    for line in corpus_lines:
        # Remove scene/music directions
        line = re.sub(r'\[.*?\]', '', line)

        # Remove repeated words (basic)
        line = re.sub(r'\b(\w+)( \1\b)+', r'\1', line)

        # Strip punctuation and extra spaces
        line = line.strip().lower()
        cleaned.append(line)
    return cleaned

# Token cleaning
def clean_tokens(tokens):
    return [t.strip(string.punctuation) for t in tokens if t.strip()]

# N-gram model class
class NGramModel:
    def __init__(self, n):
        self.n = n
        self.ngrams_freq = defaultdict(Counter)

    def train(self, text_corpus):
        tokens = clean_tokens(text_corpus.lower().split())
        for gram in ngrams(tokens, self.n, pad_left=True, pad_right=True,
                           left_pad_symbol='<s>', right_pad_symbol='</s>'):
            prefix = gram[:-1]
            next_word = gram[-1]
            self.ngrams_freq[prefix][next_word] += 1

    # Backoff prediction with random sampling
    def predict_next(self, context):
        tokens = clean_tokens(context.lower().split())

        for backoff_n in range(self.n - 1, 0, -1):
            prefix = tuple(tokens[-backoff_n:]) if backoff_n > 0 else ()
            possible_words = self.ngrams_freq.get(prefix, None)

            if possible_words:
                # Sample based on frequency
                return random.choices(
                    list(possible_words.keys()),
                    weights=possible_words.values()
                )[0]

        return "<no prediction>"











