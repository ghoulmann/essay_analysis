# -*- coding: utf-8 -*-
import os, sys
import textract
from mimetypes import MimeTypes
import nltk
from nltk import tokenize
from nltk import pos_tag
from passive.passive import main as passive
import re
from collections import Counter
from nltk import FreqDist
from nltk.corpus import cmudict
from curses.ascii import isdigit
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import nltk
from textstat.textstat import textstat
import math


"""
Creates document instance for analysis.

Opens and reads document to string raw_text.
A revision of document_in that relies on
textract.
"""

#from mimetypes import MimeTypes

class Sample:
    def __init__(self, path):
        self.user = ""
        self.path = path
        self.abs_path = os.path.abspath(self.path)
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(path)
            self.mime = MimeTypes()
            self.guessed_type = self.mime.guess_type(self.path)
            self.file_type = self.guessed_type[0]
            self.raw_text = textract.process(self.path)
            self.ptext = re.sub(u'[\u201c\u201d]','"',self.raw_text)
            self.ptext = re.sub(u"\u2014", "--", self.ptext)
            self.ptext = re.sub(",", ",", self.ptext)
            self.ptext = re.sub("—", "--", self.ptext)
            self.ptext = re.sub("…", "...", self.ptext)
            self.text_no_feed = self.clean_new_lines(self.ptext)
            # self.sentence_tokens = tokenize.sent_tokenize(self.text_no_feed)
            self.sentence_tokens = self.sentence_tokenize(self.text_no_feed)
            if self.sentence_tokens:
                self.sentence_count = len(self.sentence_tokens)
            try:
                self.passive_sentences = passive(self.text_no_feed)
                self.passive_sentence_count = len(self.passive_sentences)
                self.percent_passive = (100 * \
                (float(self.passive_sentence_count)/float(self.sentence_count)))
                self.be_verb_analysis =             self.count_be_verbs(self.sentence_tokens)
                self.be_verb_count = self.be_verb_analysis[0]
                self.weak_sentences_all = self.be_verb_analysis[1]
                self.weak_sentences_set = set(self.weak_sentences_all)
                self.weak_sentences_count = len(self.weak_sentences_set)
                self.weak_verbs_to_sentences = str(100 *        float(self.weak_sentences_count)/float(self.sentence_count)) + " %"
            except:
                print("Error: Could not process passive voice analyses.")
                print("Error: Could not process verb analyses.")
            self.word_tokens = self.word_tokenize(self.text_no_feed)
            self.word_tokens_no_punct = self.word_tokenize_no_punct(self.text_no_feed)
            if self.word_tokens_no_punct:
                self.word_count = len(self.word_tokens_no_punct)
                self.page_length = float(self.word_count)/float(250)
                self.paper_count = int(math.ceil(self.page_length))
                self.parts_of_speech = pos_tag(self.word_tokens_no_punct)
                self.pos_counts = Counter(tag for word,tag in self.parts_of_speech)
                self.pos_total = sum(self.pos_counts.values())
                self.pos_freq = dict((word, float(count)/self.pos_total) for word,count in self.pos_counts.items())
            if self.word_count:
                self.doc_pages = float(float(self.word_count)/float(250))
            elif self.word_tokens_no_punct:
                self.doc_pages = float(float(self.word_tokens_no_punct)/float(250))
            else:
                self.doc_pages = False
            self.freq_words = self.word_frequency(self.word_tokens_no_punct)

            self.ws_tokens = self.ws_tokenize(self.text_no_feed)
            self.word_tokens_no_punct = self.tokenize_no_punctuation(self.text_no_feed)
            self.readabilty_flesh_re =
                textstat.flesch_reading_ease(self.text_no_feed)
            self.readability_smog_index =
                textstat.smog_index(self.text_no_feed)
            self.readability_flesh_kincaid_grade =
                textstat.flesch_kincaid_grade(self.text_no_feed)
            self.readability_coleman_liau_index =
                textstat.coleman_liau_index(self.text_no_feed)
            self.readability_ari =
                texstat.automated_readability_index(self.text_no_feed)



    def tokenize_no_punctuation(self, text):
        text.translate(None, '!@#;.?!\":')
        return self.ws_tokenize(text)

    def ws_tokenize(self, text):
        self.tokenizer = nltk.tokenize.regexp.WhitespaceTokenizer()
        text = text.lower()
        return self.tokenizer.tokenize(text)

    """
    Breaks the program - from an earlier version
    def ws_tokenize(self, text):
        self.tokenizer = nltk.tokenize.regexp.WhitespaceTokenizer()
        text = text.lower
        return self.tokenizer.tokenize(text)

    """

    def syllables_per_word(self, text):
        self.word_syllables = []
        for word in text:
            self.word_syllables.append([word, textstat.textstat.syllable_count(word)])
        return self.word_syllables

    def polysyllables(self, text):
        return textstat.textstat.polysyllabcount(text)

    def word_frequency(self, words):
        #words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        self.word_dist = FreqDist(words)
        return self.word_dist.most_common(50)

    def word_tokenize_no_punct(self, text):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)

    def word_tokenize(self, paragraph):
        try:
            self.word_tokens = tokenize.word_tokenize(paragraph)
            return self.word_tokens
        except:
            print("Error: Cannot perform word analyses.")
            return False
    def sentence_tokenize(self, paragraphs):
        try:
            self.sentences = tokenize.sent_tokenize(paragraphs)
            return self.sentences
        except:
            print "Could not tokenize text."
            return False
    def clean_new_lines(self, paragraphs):
        self.text_no_cr = paragraphs.replace("\n\n", "TOADIES").replace("\r", " ").replace("\n", " ").replace("TOADIES", "\n")
        return self.text_no_cr

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

    def syllable_count(self, word):
           self.d = cmudict.dict()
           return min([len([y for y in x if isdigit (y[-1])]) for x in self.d[str(word).lower()]])
