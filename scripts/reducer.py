#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    word, count_str = line.split('\t', 1)
    try:
        count = int(count_str)
    except ValueError:
        continue

    if word == current_word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Don't forget the last word
if current_word is not None:
    print(f"{current_word}\t{current_count}")