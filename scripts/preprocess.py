import csv
import sys

# Increase the CSV field size limit to handle large email bodies
csv.field_size_limit(sys.maxsize)

input_csv = 'data/emails.csv'
output_txt = 'data/emails.txt'

with open(input_csv, 'r', encoding='utf-8', errors='ignore') as infile, \
     open(output_txt, 'w', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    header = next(reader)          # skip header row
    print("CSV columns:", header)  # let's see the column names

    # Find the column containing the message text
    # Common column names: 'message', 'content', 'body', 'text'
    possible_names = ['message', 'content', 'body', 'text']
    msg_idx = None
    for i, col in enumerate(header):
        if col.lower() in possible_names:
            msg_idx = i
            break

    if msg_idx is None:
        print("Could not find message column. Please check the column names above.")
        sys.exit(1)

    print(f"Using column '{header[msg_idx]}' (index {msg_idx}) for email text.")

    for row in reader:
        if len(row) > msg_idx:
            message = row[msg_idx].strip()
            if message:
                # Replace newlines inside the message with spaces
                message = message.replace('\n', ' ').replace('\r', ' ')
                outfile.write(message + '\n')

print("Preprocessing complete. Output written to data/emails.txt")