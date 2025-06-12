import os
import re
import sys
from collections import Counter

SUPPRESSION_MARKERS = [
    'I am an AI',
    'misinformation',
    'disclaimer'
]


def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_phrases(text):
    # simple split on whitespace and punctuation for now
    words = re.findall(r"[A-Za-z']+", text.lower())
    return Counter(words)


def highlight_markers(text):
    lines = text.splitlines()
    flagged = []
    for line in lines:
        for marker in SUPPRESSION_MARKERS:
            if marker.lower() in line.lower():
                flagged.append(line.strip())
                break
    return flagged


def compare(a_path, b_path):
    text_a = load_text(a_path)
    text_b = load_text(b_path)
    phrases_a = set(extract_phrases(text_a))
    phrases_b = set(extract_phrases(text_b))
    shared = phrases_a & phrases_b
    unique_a = phrases_a - phrases_b
    unique_b = phrases_b - phrases_a

    print('Shared phrases:', ', '.join(sorted(shared)))
    print('\nUnique to', os.path.basename(a_path) + ':', ', '.join(sorted(unique_a)))
    print('\nUnique to', os.path.basename(b_path) + ':', ', '.join(sorted(unique_b)))

    print('\nSuppression markers in A:')
    for line in highlight_markers(text_a):
        print('  ', line)
    print('\nSuppression markers in B:')
    for line in highlight_markers(text_b):
        print('  ', line)


def main():
    if len(sys.argv) != 3:
        print('Usage: python delta_compare.py file_a file_b')
        return
    compare(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
