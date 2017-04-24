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
