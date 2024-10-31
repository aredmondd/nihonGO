import csv
import json
import os
from django.conf import settings

japaneseDict = {}

# Dynamically construct the path for the CSV file
csv_file_path = os.path.join(settings.BASE_DIR, 'theme', 'templates', 'flashcards', 'commonwords.csv')

# Load data from CSV file
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        if count > 500:
            break
        else:
            vocab_word = row[7]
            kana = row[8]
            english_translation = row[9]
            part_of_speech = row[11]
            example_sentence = row[12]
            example_sentence_kana = row[13]
            example_sentence_english = row[14]

            japaneseDict[vocab_word] = {
                'kana': kana,
                'english_translation': english_translation,
                'part_of_speech': part_of_speech,
                'example_sentence': example_sentence,
                'example_sentence_kana': example_sentence_kana,
                'example_sentence_english': example_sentence_english
            }
        count += 1

# Dynamically construct the path for saving the JSON file
json_file_path = os.path.join(settings.BASE_DIR, 'theme', 'templates', 'flashcards', 'japanesebasics.json')

# Save the dictionary to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(japaneseDict, json_file)

print("Dictionary saved to japanesebasics.json")
