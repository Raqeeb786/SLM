import yt_dlp
import os

url = "https://www.youtube.com/watch?v=QdW3rvVEZ2A&t=1071s&pp=0gcJCcYJAYcqIYzv"

ydl_opts = {
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['hi'],
    'subtitlesformat': 'srt',
    'skip_download': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # First get info
    info = ydl.extract_info(url, download=False)
    title = info.get('title', 'unknown')
    filename = f"{title}.en.srt"

    # Now download the subtitles
    ydl.download([url])

    # Check if file exists
    if os.path.exists(filename):
        print(f"✅ Captions saved to: {filename}")
    else:
        print("❌ Captions not saved. Something went wrong.")


# def extract_plain_text_from_srt(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     text_lines = []
#     for line in lines:
#         if line.strip() and not line.strip().isdigit() and '-->' not in line:
#             text_lines.append(line.strip())

#     return '\n'.join(text_lines)


# # Usage:
# plain_text = extract_plain_text_from_srt("Some Video Title.en.srt")
# print(plain_text[:1000])  # Print first 1000 characters
