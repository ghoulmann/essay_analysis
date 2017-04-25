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
            self.text_no_cr = self.raw_text.decode('utf-8').replace("\n", " ").replace("\r", " ")
            self.sentence_tokens = tokenize. \
                sent_tokenize(self.text_no_cr)
            self.sentence_count = len(self.sentence_tokens)
            #self.be_verb_examples = self.to_be_test(self.sentence_tokens)
            #self.be_verb_sentences = len(self.be_verb_examples)
            #self.be_verb_percent = (str(100 * \
            #    (float(self.be_verb_sentences)/float(self.sentence_count))) + " %")
            #self.be_verb_example = self.be_verb_examples[1]
            self.passive_sentences = passive(self.text_no_cr.decode('utf-8'))
            self.passive_sentence_count = len(self.passive_sentences)
            self.percent_passive = (100 * \
                (float(self.passive_sentence_count)/float(self.sentence_count)))
            self.be_verb_count = self.count_be_verbs(self.sentence_tokens)

    def count_be_verbs(self, sentences):
        self.verbs = [" am ", " is ", " are ", " was ", " were ", " be ", " being ", " been "]
        self.verb_count = 0
        for sentence in sentences:
            for verb in self.verbs:
                if verb in sentence:
                    self.verb_count = self.verb_count + 1

        return self.verb_count

"""
    def prepare_check(self, sentence_tokens):

        Issue sentences for to_be_check.

        Returns:
        var int count of "to be" verbs


        self.weak_verbs = 0
        for sentence in sentence_tokens:
            if self.to_be_check(sentence):
                self.weak_verbs = self.weak_verbs + 1
        return self.weak_verbs

    def to_be_check(self, sentence):

        Find to be verb occurences in a sentence.

        Iterarate through a list of be_verbs to see if any are in a sentence.


        Returns:
        var Bool


        self.weak_sentences = []
        self.verbs = [" am ", " is ", " are ", " was ", " were ", " be ", " being ", " been "]

        for verb in self.verbs:
            if verb in sentence:
                self.weak_sentences.append(sentence) # Testing
                print self.weak_sentences            # Testing
                return True
            else:
                return False
"""
