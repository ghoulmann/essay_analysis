"""Creates document instance for analysis for semantics and lexical statistics.

Opens and reads document to string raw_text. Relies on textract to handle
.txt, .odt, .pdf, docx, and .doc.
"""

# -*- coding: utf-8 -*-
import os, sys
import textract
from mimetypes import MimeTypes # Not necessary, we think
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




#from mimetypes import MimeTypes

class Sample:
    """Represents a document analysis.

    Uses textract to read document into a long string.  The methods are various
    sequences to get information to help make decisions for deliberate academic
    writing.
    """

    def __init__(self, path):
        """
        Create document instance for analysis.

        Opens and reads document to string raw_text.
        Textract interprets the document format and
        opens to plain text string (docx, pdf, odt, txt)

        Args:
        path (str): path to file to open, anaylze, close


        Public attributes:
        -user: (str) optional string to set username.
        -path: (str) relative path to document.
        -abs_path: (str) the absolute path to the document.
        -file_name:  (str) the file name with extension of document (base
        name).
        -mime:  tbd
        -guessed_type:  makes best guess of mimetype of document.
        -file_type:  returns index[0] from guessed_type.
        -raw_text:  (str) plain text extracted from .txt, .odt, .pdf, .docx,
        and .doc.
        -ptext:  (str) raw text after a series of regex expressions to
        eliminate special characters.
        -text_no_feed:  (str) ptext with most new line characters eliminated
        /n/n stays intact.
        -sentence_tokens:  list of all sentences in a comma separated list
        derived by nltk.
        -sentence_count:  (int) count of sentences found in list.
        -passive_sentences:  list of passive sentences identified by the
        passive module.
        -passive_sentence_count:  count of the passive_sentences list.
        -percent_passive:  (float) ratio of passive sentences to all sentences
        in percent form.
        -be_verb_analysis:  (int) sum number of occurrences of each to be verb
        (am, is, are, was, were, be, being been).
        -be_verb_count: tbd
        -be_verb_analysis: tbd
        -weak_sentences_all:  (int) sum of be verb analysis.
        -weak_sentences_set:  (set) set of all sentences identified as
        having to be verbs.
        -weak_sentences_count:  (int) count of items in weak_sentences_set.
        -weak_verbs_to_sentences:  (float) proportion of sentences with to
        be to all sentences in percent (this might not be sound).
        -word_tokens:  list of discreet words in text that breaks
        contractions up (default nltk tokenizer).
        -word_tokens_no_punct:  list of all words in text including
        contractions but otherwise no punctuation.
        -no_punct:  (str) full text string without sentence punctuation.
        -word_tokens_no_punct:  uses white-space tokenizer to create a list
        of all words.
        readability_flesch_re:  (int) Flesch Reading Ease Score (numeric
        score) made by textstat module.
        readability_smog_index:  (int) grade level as determined by the
        SMOG algorithum made by textstat module.
        readability_flesch_kincaid_grade:  (int)  Flesch-Kincaid grade level
        of reader made by textstat module.
        readability_coleman_liau_index:  (int) grade level of reader as made by
        textstat module.
        readability_ari:  (int) grade leader of reader determined by
        automated readability index algorithum implemented by textstat.
        readability_linser_write:  FIX SPELLING grade level as determined
        by Linsear Write algorithum implemented by textstat.
        readability_dale_chall:  (int) grade level based on Dale-Chall
        readability as determined by textstat.
        readability_standard:  composite grade level based on readability
        algorithums.
        -flesch_re_key:  list for interpreting Flesch RE Score.
        -word_count:  word count of document based on white space tokener,
        this word count should be used.
        -page_length:  (float) page length in decimal format given 250
        words per page.
        -paper_count:  (int) number of printed pages given 250 words per
        page.
        -parts_of_speech:  words with parts of speech tags.
        -pos_counts:  values in word, tag couple grouped in a list.
        -pos_total:  (int) sum of pos_counts values
        -pos_freq:  (dict) word, ratio of whole
        -doc_pages:  (float) page length based on 250 words per page
        (warning, this is the second time this attribute is defined).
        -freq_words:  word frequency count not standardized based on the
        correct word tokener (not ratio, just count).
        modal_dist:  count of auxillary verbs based on word_tokens_no_punct.
        sentence_count (int): Count the sentence tokens
        passive_sentences (list): List of all sentences identified as passive
        passive_sentence_count (int): count of items in passive_sentences
        be_verb_count (int): count "to be" verbs in text
        word_tokens_no_punct (list): words separated, stripped of punctuation, made lower case
        flesch_re_key (str): reading ease score to description
        freq_words (list or dict): frequency distribution of all words
        modal_dist (list): frequency distribution of aux verbs
        """
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
            # self.sentence_tokens = tokenize.sent_tokenize(self.text_no_feed) # probably to be deleted. Does not work
            self.sentence_tokens = self.sentence_tokenize(self.text_no_feed)
            if self.sentence_tokens:
                self.sentence_count = len(self.sentence_tokens)
            try:
                self.passive_sentences = passive(self.text_no_feed)
                self.passive_sentence_count = len(self.passive_sentences)
                self.percent_passive = (100 * \
                (float(self.passive_sentence_count)/float(self.sentence_count)))

                self.be_verb_analysis = \
                    self.count_be_verbs(self.sentence_tokens)
                # Remove
                #self.be_verb_analysis = \
                    #self.count_be_verbs(self.sentence_tokens)
                self.be_verb_count = self.be_verb_analysis[0]
                self.weak_sentences_all = self.be_verb_analysis[1]
                self.weak_sentences_set = set(self.weak_sentences_all)
                self.weak_sentences_count = len(self.weak_sentences_set)
                self.weak_verbs_to_sentences = str(100 * float(self.weak_sentences_count)/float(self.sentence_count)) + " %"
            except:
                print("Error: Could not process passive voice analyses.")
                print("Error: Could not process verb analyses.")
            self.word_tokens = self.word_tokenize(self.text_no_feed)
            self.word_tokens_no_punct = self.word_tokenize_no_punct(self.text_no_feed)
            self.no_punct = self.strip_punctuation(self.text_no_feed)
            # use this! It make lower and strips symbols
            self.word_tokens_no_punct = self.ws_tokenize(self.no_punct)
            self.readability_flesch_re = \
                textstat.flesch_reading_ease(self.text_no_feed)
            self.readability_smog_index = \
                textstat.smog_index(self.text_no_feed)
            self.readability_flesch_kincaid_grade = \
                textstat.flesch_kincaid_grade(self.text_no_feed)
            self.readability_coleman_liau_index = \
                textstat.coleman_liau_index(self.text_no_feed)
            self.readability_ari = \
                textstat.automated_readability_index(self.text_no_feed)
            self.readability_linser_write = \
                textstat.linsear_write_formula(self.text_no_feed)
            self.readability_dale_chall = \
                textstat.dale_chall_readability_score(self.text_no_feed)
            self.readability_standard = \
                textstat.text_standard(self.text_no_feed)
            self.flesch_re_key = (
                "* 90-100 : Very Easy",
                "* 80-89 : Easy",
                "* 70-79 : Fairly Easy",
                "* 60-69 : Standard",
                "* 50-59 : Fairly Difficult",
                "* 30-49 : Difficult",
                "* 0-29 : Very Confusing"
                )
            if self.word_tokens_no_punct:
                self.word_count = len(self.word_tokens_no_punct)
                self.page_length = float(self.word_count)/float(250)
                self.paper_count = int(math.ceil(self.page_length))
                self.parts_of_speech = pos_tag(self.word_tokens_no_punct)
                self.pos_counts = Counter(tag for word,tag in self.parts_of_speech)
                self.pos_total = sum(self.pos_counts.values())
                self.pos_freq = dict((word, float(count)/self.pos_total) for word,count in self.pos_counts.items())
                self.doc_pages = float(float(self.word_count)/float(250)) \
                    #duplicate
                self.freq_words = \
                    self.word_frequency(self.word_tokens_no_punct)
                self.modal_dist = self.modal_count(self.word_tokens_no_punct)
                #self.ws_tokens = self.ws_tokenize(self.text_no_cr)

    def strip_punctuation(self, string_in):
        """
        Strip punctuation from string and make lower

        Given a string of sentences, translate string
        to remove some common symbols and conver caps
        to lower case.

        Args:
        string_in (str): Text to strip punctuation from

        return:
        str
        """
        string_in = string_in.translate(None, ',.!?\"<>{}[]--@()\'--')
        return str(string_in.lower())

    """
    def ws_tokenize(self, text):
        Given string of words, return word tokens with contractions OK

        Other tokenizers tokenize punctuation. The WhitespaceTokenizer
        is important because of contractions.

        Args:
        text (str)

        returns:
        list


        self.tokenizer = nltk.tokenize.regexp.WhitespaceTokenizer()
        return self.tokenizer.tokenize(text)
    """

    def syllables_per_word(self, text):
        self.word_syllables = []
        for word in text:
            self.word_syllables.append([word, textstat.textstat.syllable_count(word)])
        return self.word_syllables

    def polysyllables(self, text):
        """
        Given sting of full text, count polysllables.

        Count words in text string that have >= 3 syllables.

        Args:

        text (str)

        Returns:
        int: polysllable word count in text arg

        """
        return textstat.textstat.polysyllabcount(text)

    def word_frequency(self, words):
        #words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        self.word_dist = FreqDist(words)
        return self.word_dist.most_common(50)

    def word_tokenize_no_punct(self, text):
        """
        Make list of words without listing punctuation

        Args:
            text (str): Plain text string

        Returns:
             list of words
        """
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
        """
        Strips new line characters except for new paragraphs

        """

        self.text_no_cr = paragraphs.replace("\n\n", "TOADIES").replace("\r", " ").replace("\n", " ").replace("TOADIES", "\n")
        return self.text_no_cr

    def count_be_verbs(self, sentences):
        """
        Count be verbs in each sentence in a list.

        Loop through sentences to provide weak verb count.
        If count >= 1, add sentence to list.

        Args:
            sentences (str, list)

        Return:
            list of be-verb count and stand-out sentences

        """
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
           """
           Count syllables in a word.

           Uses NLTK dictionary to find word syllabication.

           Args:
               word (string)

           Returns:
               int syllable count
           """
           self.d = cmudict.dict()
           return min([len([y for y in x if isdigit (y[-1])]) for x in self.d[str(word).lower()]])

    def modal_count(self, text):
        """
        Return FreqDist of modal verbs in text
        """
        fdist = FreqDist(w.lower() for w in text)
        modals = ['can', 'could', 'shall', 'should', 'will', 'would', 'do', 'does', 'did', 'may', 'might', 'must', 'has', 'have', 'had']
        modals_freq = []
        for m in modals:
            modals_freq.append(str(m + ': ' + str(fdist[m])))
        return modals_freq
