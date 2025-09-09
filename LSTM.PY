import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.utils import to_categorical

# 1. Load your text data (example: all captions concatenated)
with open('final_captions.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 2. Clean and preprocess text (basic)
text = text.replace('\n', ' ').lower()

# 3. Tokenize words
tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
total_words = len(tokenizer.word_index) + 1

# 4. Create input sequences (using sliding window)
input_sequences = []
tokens = tokenizer.texts_to_sequences([text])[0]

seq_length = 5  # number of words in input sequence
for i in range(seq_length, len(tokens)):
    seq = tokens[i-seq_length:i+1]  # input seq + next word
    input_sequences.append(seq)

input_sequences = np.array(input_sequences)

# Split into inputs and labels
X = input_sequences[:, :-1]  # first 5 words
y = input_sequences[:, -1]   # next word

# One-hot encode labels
y = to_categorical(y, num_classes=total_words)

# 5. Build LSTM model
model = Sequential([
    Embedding(total_words, 100, input_length=seq_length),
    LSTM(150, return_sequences=True),
    LSTM(100),
    Dense(total_words, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# 6. Train model
model.fit(X, y, epochs=20, batch_size=128)

# 7. Function to predict next word
def predict_next_word(model, tokenizer, text_seq, max_seq_len=seq_length):
    text_seq = text_seq.lower().split()
    text_seq = text_seq[-max_seq_len:]  # last max_seq_len words
    encoded = tokenizer.texts_to_sequences([' '.join(text_seq)])[0]
    encoded = pad_sequences([encoded], maxlen=max_seq_len, padding='pre')
    
    pred_prob = model.predict(encoded, verbose=0)[0]
    pred_index = np.argmax(pred_prob)
    predicted_word = tokenizer.index_word.get(pred_index, '')
    
    return predicted_word

# 8. Test example
test_phrases = [
    "क्या तुम भी",
    "वैसे आज का मौसम",
    "क्या तुमने होमवर्क",
    "अरे कहां जा रे",
    "कहा जा रे",
    "घर कब तक",
    "सबसे आज"
]

for phrase in test_phrases:
    next_word = predict_next_word(model, tokenizer, phrase)
    print(f"Input: {phrase} -> Next word: {next_word}")
