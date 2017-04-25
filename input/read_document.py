# -*- coding: utf-8 -*-
import os, sys
import textract
from mimetypes import MimeTypes
from nltk import tokenize
from passive.passive import main as passive
import codecs
"""
Creates document instance for analysis.

Opens and reads document to string raw_text.
A revision of document_in that relies on
textract.
"""

#from mimetypes import MimeTypes

class Sample:
    def __init__(self, path, *writer):
        self.path = path
        if writer:
            self.writer = writer
        self.abs_path = os.path.abspath(self.path)
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(path)
            self.mime = MimeTypes()
            self.guessed_type = self.mime.guess_type(self.path)
            self.file_type = self.guessed_type[0]
            self.raw_text = textract.process(self.path)
            self.text_no_cr = self.raw_text.replace("\n", " ").replace("\r", " ")
            self.sentence_tokens = tokenize. \
                sent_tokenize(self.text_no_cr)
            self.sentence_count = len(self.sentence_tokens)
            self.passive_sentences = passive(self.text_no_cr.decode('utf-8'))
            self.passive_sentence_count = len(self.passive_sentences)
            self.percent_passive = (100 * \
                (float(self.passive_sentence_count)/float(self.sentence_count)))
            self.be_verb_analysis = self.count_be_verbs(self.sentence_tokens)
            self.be_verb_count = self.be_verb_analysis[0]
            self.weak_sentences_all = self.be_verb_analysis[1]
            self.weak_sentences_set = set(self.weak_sentences_all)
            self.weak_sentences_count = len(self.weak_sentences_set)
            self.weak_verbs_to_sentences = str(100 * float(self.weak_sentences_count)/float(self.sentence_count)) + " %"

    def count_be_verbs(self, sentences):
        self.verbs = [" am ", " is ", " are ", " was ", " were ", " be ", " being ", " been "]
        self.weak_sentences = []
        self.verb_count = 0
        for sentence in sentences:
            for verb in self.verbs:
                if verb in sentence:
                    self.verb_count = self.verb_count + 1
                    self.weak_sentences.append(sentence)


        return [self.verb_count, self.weak_sentences]
