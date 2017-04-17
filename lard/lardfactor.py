"""
count percent of verbs that are auxiary verbs
"""

import nltk

def process_file_for_adjectives(file):
    """
    open and prepare a (txt) file for passive voice report.

    Open file, read each sentence into a list of strings,
    remove (clean) new line and line feed characters.

    :param: string, filename

    :returns: raw_text
    """

    # mime = MimeTypes()
    # mime_type = mime.guess_type(file)
    #if mime_type[0] == "text/plain":
    fh = open(file, "r")
    raw_text = fh.read()
    fh.close()
    raw_text = raw_text.replace("\n", "").replace("\r", "")
    raw_text_list = raw_text.split(". ")


    return raw_text

def process_file_for_modals(file):
    """
    open and prepare a (txt) file for passive voice report.

    Open file, read each sentence into a list of strings,
    remove (clean) new line and line feed characters.

    :param: string, filename

    :returns: raw_text
    """

    # mime = MimeTypes()
    # mime_type = mime.guess_type(file)
    #if mime_type[0] == "text/plain":
    fh = open(file, "r")
    raw_text = fh.read()
    fh.close()
    raw_text = raw_text.replace("\n", "").replace("\r", "")
    raw_text_list = raw_text.split(". ")


    return raw_text_list

def aux_verb_test(sentence):
    verbs = ["am", "is", "are", "was", "were", "be", "being",
        "been", "may", "might", "must", "can", "could", "shall",
	"should", "will", "would", "do", "does", "did", "has", "have",
	"had", "do", "has", "have", "had"]

    for verb in verbs:
        if verb in sentence:
            return True
        else:
            return False
def adjective_work(text):
    adjectives = [token for token, pos in
        nltk.pos_tag(nltk.word_tokenize(text))
        if pos.startswith('JJ')]
    return len(adjectives)

def main():

    raw_text = process_file_for_adjectives("../data/example.txt")
    #sentence_list = sentence_tokens(raw_text)
    #print len(sentence_list)
    #tags_list = []
    #for sentence in sentence_list:
    #   tags_list.append(tagged_text(sentence))
    raw_text_list = process_file_for_modals("../data/example.txt")
    sentences = len(raw_text_list)
    aux_verb_count = 0
    for sentence in raw_text_list:
	if aux_verb_test(sentence):
            aux_verb_count = aux_verb_count + 1
    print("Lard Factor Indicators\n=================================\n\n")
    print("* Sentences with auxiliary verbs: " + str(100 * float(aux_verb_count)/float(len(raw_text_list))) + " %")      
    print("* Diluted Noun Strings (prepositions): "
        + str(adjective_work(raw_text)) + " (total sentences = " + str(sentences) + ")")
    print("* passive voice indication: "),

main()
