#!/usr/bin/env python

"""passive.py: First pass at finding passive voice sentences, and more
importantly, getting familiar with NLTK.

Tags a sentence with a way-overkill four-level tagger trained from the Brown
Corpus, and then looks at its verbs. If somewhere in the sentence, there's a
to-be verb and then later on a non-gerund, we'll flag the sentence as probably
passive voice.

Developed against NLTK 2.0b5.
Copied from http://narorumo.googlecode.com in late April 2013"""

import nltk
import sys
import os
from itertools import dropwhile
import postagger

TAGGER = None

#def sentence_count(fn):
#    fh = open(fn)
#    raw_text = fh.read()
#    clean = raw_text.replace("\n", "").replace("\r", "")
#    sentences = nltk.sent_tokenize(clean)
#    all_sentences = len(sentences)

#    return all_sentences
def tag_sentence(sent):
    """Take a sentence as a string and return a list of (word, tag) tuples."""
    assert isinstance(sent, basestring)

    tokens = nltk.word_tokenize(sent)
    return TAGGER.tag(tokens)

def passivep(tags):
    """Takes a list of tags, returns true if we think this is a passive
    sentence."""
    # Particularly, if we see a "BE" verb followed by some other, non-BE
    # verb, except for a gerund, we deem the sentence to be passive.

    postToBe = list(dropwhile(lambda(tag): not tag.startswith("BE"), tags))
    nongerund = lambda(tag): tag.startswith("V") and not tag.startswith("VBG")

    filtered = filter(nongerund, postToBe)
    out = any(filtered)

    return out

def oneline(sentence):
    """Replace CRs and LFs with spaces."""
    return sentence.replace("\n", " ").replace("\r", " ")

def list_if_passive(sentence):
    """Given a sentence, tag it and print if we think it's a passive-voice
    formation."""
    tagged = tag_sentence(sentence)
    tags = map( lambda(tup): tup[1], tagged)
    if passivep(tags):
        #print "* passive:", oneline(sent)
        #fh = open("./results.txt", "a")
        passive_sentence = sentence
        if passive_sentence:
            return passive_sentence
        else:
            return False
# punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
def findpassives(clean_text):
    punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
    sentences = punkt.tokenize(clean_text)
    passive_sentences = []
    for sentence in sentences:
        if list_if_passive(sentence):
            passive_sentences.append(list_if_passive(sentence))
        #    passive_sentences.append(print_if_passive(sent))
    return passive_sentences
def repl():
    """Read eval (for passivity) print loop."""
    try:
        while True:
            line = raw_input()
            print_if_passive(line)
    except EOFError,e:
        pass

#def report(filename, passive_count, sentence_count, passive_sentences):

#    percent_passive = 100 * (float(passive_count)/float(sentence_count))
#    header = "Passive Voice Anaylsis: " + filename \
#        + "\n=============================================\n\n"
#    summary = []
#    summary.append(header)
#    summary.append("Passive Voice Summary\n--------------------------\n\n")
#    summary.append("Passive Sentence Count: " + str(passive_count) + "\n\n")
#    summary.append("Total Sentence Count: " + str(sentence_count) + "\n\n")
#    summary.append("Percent Passive : " + str(percent_passive) + "\n\n")
#    summary.append("\nDetails\n------------------\n\n")
#    for sentence in passive_sentences:
#        summary.append(sentence)
#    fh = open("/tmp/report.md", "a")
#    for item in summary:
#        fh.write(item)
#    fh.close()
def main(clean_text):
    global TAGGER
    TAGGER = postagger.get_tagger()
    passive_sentences = findpassives(clean_text)
    # all_sentences = sentence_count(clean_text)
    # if len(sys.argv) > 1:
    #    for fn in sys.argv[1:]:

    #        print "------------------------------------"
    #        passive_sentences = findpassives(fn)
    #        print type(passive_sentences)
    #        print len(passive_sentences)
    #        for sentence in passive_sentences:
    #            print sentence
            #sentences = fn
        #sentences = sentences.replace("\n", "").replace("\r", "")
        #sentences = nltk.sent_tokenize(sentences)
        #    all_sentences = sentence_count(fn)
        #sentence_count = len(sentences)
    #else:
    #    repl()
    # for report
    #fn = sys.argv[1]
    #fh = open("results.txt", "r")
    #passive_sentences = fh.readlines()
    #fh.close
    #report(fn, len(passive_sentences), float(all_sentences), passive_sentences)
    return passive_sentences
    print len(passive_sentences)
    print type(passive_sentences)
    for sentence in passive_sentences:
        print sentence
    #delete results_file

    #os.remove("./results.txt")

if __name__ == "__main__":
    main()
