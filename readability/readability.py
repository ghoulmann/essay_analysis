from textstat.textstat import textstat


fh = open("../samples/example.txt", "r")
raw_text = fh.read()
fh.close()

text = raw_text.replace("\n", "").replace("\r", "")

def readability(text):
    print("Readability\n=================================\n\n")
    print("Flesch Reading Ease\n________________________\n\n")
    print str(textstat.flesch_reading_ease(text)) + "\n"
    print("Smog Index\n________________________\n\n")
    print str(textstat.smog_index(text)) + "\n"
    print("Flesch Kincaid Grade\n________________________\n\n")
    print str(textstat.flesch_kincaid_grade(text)) + "\n"
    print("Coleman Liau Index\n________________________\n\n")
    print str(textstat.coleman_liau_index(text)) + "\n"
    print("ARI\n________________________\n\n")
    print str(textstat.automated_readability_index(text)) + "\n"
    print("Dale Chall\n________________________\n\n")
    print str(textstat.dale_chall_readability_score(text)) + "\n"
    print("Difficult Words\n________________________\n\n")
    print str(textstat.difficult_words(text)) + "\n"
    print("Linsear Write Formula\n________________________\n\n")
    print str(textstat.linsear_write_formula(text)) + "\n"
    print("Gunning Fog\n________________________\n\n")
    print str(textstat.gunning_fog(text)) + "\n"
    print "Compiled Score\n_____________________________\n\n"
    print str(textstat.text_standard(text)) + "\n"


    return len(adjectives)
readability(text)
