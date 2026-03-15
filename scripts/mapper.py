import sys
import re

# Comprehensive list of stop words to make the results meaningful
STOP_WORDS = {
    'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'for', 
    'on', 'was', 'as', 'with', 'be', 'by', 'at', 'this', 'from', 'i', 'have', 
    'or', 'will', 'an', 'my', 'been', 'if', 'are', 'we', 'not', 'me', 'your'
}

def tokenize(text):
    # Matches words with at least 3 characters, avoiding long repetitive sequences like "aaaaa"
    # This regex ensures the word doesn't have the same character repeated more than 3 times in a row
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return [w for w in words if not re.search(r'(.)\1{3,}', w)]

for line in sys.stdin:
    # Strip leading/trailing whitespace to avoid issues
    line = line.strip()
    words = tokenize(line)
    
    for word in words:
        if word not in STOP_WORDS:
            # Hadoop Streaming expects a tab-separated key-value pair
            print(f"{word}\t1")