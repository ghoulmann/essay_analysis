import textract
import sys
import nltk

file_location = sys.argv[1]
raw_text = textract.process(file_location)
raw_text = raw_text.replace("\n\n", "LEAPFROG").replace("\n", " ").replace("LEAPFROG", "\n")
raw_text = raw_text.decode('utf-8')

print raw_text
