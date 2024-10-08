#this program parses the 500 most commonly used words in japanese into a python dictionary'
#this dictionary is what will be used to create the users starter deck in NihonGO!

import csv 
japaneseDict = {}
with open('/Users/laurenrichardson/Desktop/commonWords.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    
    # Skip the header row if it exists
    next(reader, None)
    
    # Loop through each row in the CSV
    count = 0
    for row in reader:
        if count > 500:
            break
        else:
            #index 7 is vocab word
            #index 8 is kana (pronounciation)
            #index 9 is english translation
            #index 11 is part of speech 
            #index 12 is example sentence
            #index 13 is example sentence kana (pronunciation)
            #index 14 is example sentence english translation

            vocab_word = row[7] 
            kana = row[8]  
            english_translation = row[9]  
            part_of_speech = row[11] 
            example_sentence = row[12] 
            example_sentence_kana = row[13] 
            example_sentence_english = row[14] 

        # Store the extracted values in a dictionary for each vocab word
        japaneseDict[vocab_word] = {
            'kana': kana,
            'english_translation': english_translation,
            'part_of_speech': part_of_speech,
            'example_sentence': example_sentence,
            'example_sentence_kana': example_sentence_kana,
            'example_sentence_english': example_sentence_english
        }

print(japaneseDict)