import csv
import re

def parse_srt_to_csv(srt_file, csv_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        srt_content = f.read()

    # Split into blocks by two newlines
    blocks = srt_content.strip().split('\n\n')

    # Prepare rows for CSV
    rows = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = lines[0]
            time_range = lines[1]
            text = " ".join(lines[2:]).replace('\n', ' ').strip()

            # Extract start and end times
            match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})', time_range)
            if match:
                start_time, end_time = match.groups()
                rows.append([index, start_time, end_time, text])

    # Write to CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Index', 'Start Time', 'End Time', 'Text'])  # header
        writer.writerows(rows)

    print(f"✅ CSV saved to: {csv_file}")


# 🔧 Usage:
srt_file = 'mere_humsafar.srt'
csv_file = 'captions.csv'
parse_srt_to_csv(srt_file, csv_file)
