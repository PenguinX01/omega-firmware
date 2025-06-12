import csv
import os
from datetime import datetime

FIELDS = [
    'date', 'evaluator', 'topic', 'frame', 'model',
    'factual', 'normative', 'deflection', 'suppression_flags', 'notes'
]
CSV_PATH = os.path.join(os.path.dirname(__file__), 'img_scores.csv')

def prompt_int(field):
    while True:
        val = input(f'{field} (0-2): ').strip()
        if val.isdigit() and 0 <= int(val) <= 2:
            return int(val)
        print('Please enter 0, 1, or 2.')

def main():
    evaluator = input('Evaluator initials: ').strip()
    topic = input('Topic: ').strip()
    frame = input('Frame: ').strip()
    model = input('Model: ').strip()
    factual = prompt_int('Factual')
    normative = prompt_int('Normative')
    deflection = prompt_int('Deflection')
    suppression_flags = input('Suppression flags: ').strip()
    notes = input('Notes: ').strip()

    row = [
        datetime.utcnow().isoformat(), evaluator, topic, frame, model,
        factual, normative, deflection, suppression_flags, notes
    ]

    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(FIELDS)
        writer.writerow(row)
    print('Entry recorded in', CSV_PATH)

if __name__ == '__main__':
    main()
