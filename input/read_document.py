# -*- coding: utf-8 -*-
import os, sys
import textract
from mimetypes import MimeTypes
from nltk import tokenize
"""
Creates document instance for analysis.

Opens and reads document to string raw_text.
A revision of document_in that relies on
textract.
"""

#from mimetypes import MimeTypes

class Sample:
    def __init__(self, path, *author):
        self.path = path
        self.author = author
        self.abs_path = os.path.abspath(self.path)
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(path)
            self.mime = MimeTypes()
            self.guessed_type = self.mime.guess_type(self.path)
            self.file_type = self.guessed_type[0]
            self.raw_text = textract.process(self.path)
            self.text_no_cr = self.raw_text.replace("\n", " ").replace("\r", " ")
            self.sentence_tokens = tokenize.sent_tokenize(self.text_no_cr)
            self.sentence_count = len(self.sentence_tokens)
            self.be_verb_examples = self.to_be_test(self.sentence_tokens)
            self.be_verb_sentences = len(self.be_verb_examples)
            self.be_verb_precent = (str(100 * \
                (float(self.be_verb_sentences)/float(self.sentence_count))) + " %")
            self.be_verb_example = self.be_verb_examples[1]
    def to_be_test(self, sentence_list):
        """
        Find to be verb occurences in list of sentences.

        Currently not working correctly; for each verb in be_verbs
        iterate through sentences looking for sentences with the word.

        Returns:

        list: weak_sentences
        """
        self.weak_sentences = []
        self.be_verbs = ["am", "is", "are", "was", "were", "be",
            "being", "been"]
        for word in self.be_verbs:
            for sentence in sentence_list:
                if word in sentence:
                    self.weak_sentence = str("Weak Verb: " + sentence)
                    self.weak_sentences.append(self.weak_sentence)

        return self.weak_sentences
