import os
import re
import csv
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def save_translated_captions_to_csv(video_id, output_file):
    try:
        # Get all available transcripts for the video
        ytt_api= YouTubeTranscriptApi()
        transcript_data= ytt_api.fetch(video_id,languages=['hi'])
    
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Start Time (s)', 'Duration (s)', 'Text'])  # Header
                for entry in transcript_data:
                    writer.writerow([entry.start, entry.duration, entry.text])
                print(f"📁 Captions saved successfully to '{output_file}'")

    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video.")
    except NoTranscriptFound:
        print("❌ No transcripts found in any language.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    
# Example usage
# video_id = '1cPOKARElgs'  # Replace with any YouTube video ID
# output_file = 'captions.csv'
# save_translated_captions_to_csv(video_id, output_file)



def extract_sentences_from_csv(csv_path='captions.csv', output_file='SERIALS/raw_urdu.txt'):
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
    print(f"📁 Extracted {len(sentences)} sentences to '{output_file}'")

#extract_sentences_from_csv()



# def load_lexicon(lexicon_path='lexicon.txt'):
#     all_to_urdu = {}
#     with open(lexicon_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             parts = line.strip().split(':')
#             key,value = parts[0].lower(),parts[1]
#             all_to_urdu[key]=value
#     return all_to_urdu



# def convert_sentence_with_lexicon(sentence, lexicon):
#     # Use a regex that matches words in all scripts (including Urdu/Hindi)
#     words = re.findall(r'[\w\u0600-\u06FF\u0900-\u097F]+', sentence)
#     romanized_words = []
    
#     for w in words:
#         # For English words, normalize to lowercase; for others keep as is
#         key = w.lower() if re.match(r'^[a-zA-Z]+$', w) else w
#         if key in lexicon:
#             romanized_words.append(lexicon[key])
#         else:
#             dump.append(w)
#             romanized = w
#             romanized_words.append(romanized)
#     return ' '.join(romanized_words)





# # Main pipeline function to process all captions in CSV
# def process_captions(dialogues_path='SERIALS/raw_urdu.txt', lexicon_path='lexicon.txt', output_path='SERIALS/romanized.txt'):
#     print(output_path)
#     with open(dialogues_path, 'r', encoding='utf-8') as dialogues, \
#          open(output_path, 'w', encoding='utf-8') as out_file,\
#             open(lexicon_path,'r',encoding='utf-8') as lex_file:

#         #lex= lex_file.readlines()
#         #lexicon = build_lexicon_dict(lex)
#         lexicon= load_lexicon(lexicon_path)
#         reader= dialogues.readlines()
#         for row in reader:
#             text = row.strip()
#             if not text:
#                 continue

#             # Try lexicon-based conversion
#             romanized = convert_sentence_with_lexicon(text, lexicon)

#             # # If lexicon failed (unknown word), translate and transliterate
#             # if romanized is None:
#             #     urdu_text = asyncio.run(translate_to_urdu(text))
#             #     if urdu_text:
#             #         romanized = transliterate_urdu_sentence(urdu_text.text)+'#'
#             #     else:
#             #         romanized = text  # fallback: original text if translation fails

#             out_file.write(str(romanized) + '\n')
#             #print(f"Original: {text}\nRomanized: {romanized}\n")
#     print('SUUCEESS')



if __name__ == '__main__':
    #video_id='S1V8kK4z-9k'  # Replace with any YouTube video ID
    with open('serials_code.txt','r',encoding='utf-8')as f:
        serials=f.readlines()
        count=1
        for serial in serials:
            dump=[]
            if serial[0]=='*':
                continue
            video_id=serial.strip()
            save_translated_captions_to_csv(video_id,'SERIALS/captions'+str(count)+'.csv')
            extract_sentences_from_csv(csv_path='SERIALS/captions'+str(count)+'.csv',output_file='SERIALS/captions'+str(count)+'.txt')
            #process_captions(dialogues_path='SERIALS/captions'+str(count)+'.txt',output_path='SERIALS/romanized_captions'+str(count)+'.txt')
            update_lexicon=set(dump)
            with open('dump.txt','a',encoding='utf-8')as f:
                for item in update_lexicon:
                    f.write("%s\n" % item)
            count+=1
    #next_word_predictor()







