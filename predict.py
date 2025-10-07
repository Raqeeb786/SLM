import pickle
from slm_utils import clean_tokens

# Load models
def load_model(n):
    with open(f"models/{n}gram.pkl", "rb") as f:
        return pickle.load(f)

models = {
    2: load_model(2),
    3: load_model(3),
    4: load_model(4),
}

# Run prediction loop
while True:
    user_input = input("👤 Enter Hindi phrase (or type 'exit'): ")
    if user_input.strip().lower() == 'exit':
        break

    for n, model in models.items():
        next_word = model.predict_next(user_input)
        print(f"{n}-gram prediction → {next_word}")

