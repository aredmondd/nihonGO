import csv
import json

japaneseDict = {}
with open("/Users/laurenrichardson/Desktop/nihonGO!/nihonGO/nihonGO/theme/templates/flashcards/commonwords.csv", 'r') as file:
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

# Save the dictionary to a JSON file
with open('/Users/laurenrichardson/Desktop/nihonGO!/nihonGO/nihonGO/theme/templates/flashcards/japanesebasics.json', 'w') as json_file:
    json.dump(japaneseDict, json_file)

print("Dictionary saved to japanese_data.json")
