import csv
import re

def load_terms(file_path):
    terms = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                term = parts[0].lower()
                translations = {}
                for part in parts[1:]:
                    language, translation = part.split(':')
                    translations[language] = translation
                terms[term] = translations
    return terms

def process_csv(input_file, output_file, terms):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)
        writer.writerow(headers)
        
        language_indices = {lang: i for i, lang in enumerate(headers) if lang != 'Sl No' and lang != 'Field Name'}
        
        for row in reader:
            for term, translations in terms.items():
                for lang, translation in translations.items():
                    if lang in language_indices:
                        index = language_indices[lang]
                        row[index] = re.sub(r'\b' + re.escape(term) + r'\b', 
                                            translation, 
                                            row[index], 
                                            flags=re.IGNORECASE)
            writer.writerow(row)

# Load terms from file
terms = load_terms('terms.txt')

# Process the CSV file
process_csv('file.csv', 'updated_file.csv', terms)

print("Processing complete. Updated file saved as 'updated_file.csv'.")