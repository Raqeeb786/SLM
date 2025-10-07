from datasets import load_dataset
import random
import re

def clean_text(text):
    text = text.strip()
    text = re.sub(r'[^\u0900-\u097F\s।]', '', text)  # keep only Hindi letters and danda
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    return text

def main():
    print("Streaming IndicCorp dataset...")
    dataset = load_dataset("ai4bharat/IndicCorpV2", "indiccorp_v2", split="hin_Deva", streaming=True)

    sample_size = 20000
    print(f"Sampling {sample_size} lines from stream...")

    cleaned_set = set()
    count = 0

    for item in dataset:
        if count >= sample_size:
            break
        cleaned_line = clean_text(item['text'])
        if cleaned_line:
            cleaned_set.add(cleaned_line)
            count += 1

    print(f"Collected {len(cleaned_set)} unique cleaned lines")

    output_file = "hindi_corpus_sample_cleaned.txt"
    print(f"Saving cleaned corpus to {output_file}...")

    with open(output_file, "w", encoding="utf-8") as f:
        for line in cleaned_set:
            f.write(line + "\n")

    print("Done! Corpus ready for training.")

if __name__ == "__main__":
    main()
