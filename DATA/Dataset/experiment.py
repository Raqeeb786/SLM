
        # transcript_list = ytt_api.list(video_id)

        # try:
        #     # Try to find an English transcript (preferred)
        #     transcript = transcript_list.find_transcript(['en'])
        #     print("✅ English transcript found.")
        # except NoTranscriptFound:
        #     # If English not found, get any transcript and translate to English
        #     print("ℹ️ English transcript not found. Trying to translate another language to English...")
        #     transcript = transcript_list.find_transcript([t.language_code for t in transcript_list])
        #     transcript = transcript.translate('en')
        #     print(f"✅ Translated transcript from '{transcript.language_code}' to English.")

        # # Fetch the transcript content
        # transcript_data = transcript.fetch()

        # Save to CSV
        







import os
import csv

def extract_sentences_from_csv(csv_path='captions.csv', output_file='raw_urdu.txt'):
    sentences = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['Text'].strip()
            if text:
                # Optional: remove line breaks inside quotes
                text = text.replace('\n', ' ')
                sentences.append(text)

    with open(output_file, 'w', encoding='utf-8') as out:
        for sentence in sentences:
            out.write(sentence + '\n')

#extract_sentences_from_csv()


