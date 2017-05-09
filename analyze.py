# -*- coding: utf-8 -*-

"""
Intended as the CLI entry point for the thing.
"""

import sys
import os
import argparse
from input import read_document as input

def main(path):
    """
    Output some information about the WritingSample instance to
    stdout.

    """

    Document = input.Sample(path)

    print("Base Name: " + Document.file_name)
    print("Relative path to file: " + Document.path)

    print("Absolute path to file: " + Document.abs_path)
    print("Weak Verbs to Sentences: " + str(Document.weak_verbs_to_sentences))
    print("Weak verb count: " + str(Document.be_verb_count))
    print("Percent passive sentences: " + str(Document.percent_passive) + " %")
    print("Sentence Count: " + str(Document.sentence_count))
    print("Example passive sentence from document: " + Document.passive_sentences[-1])
    print("Example weak-verb usage: " + Document.weak_sentences_all[-2])
    print("Sum of 'to be' usage:" + str(Document.be_verb_analysis))
    print("Readability (Flesch Reading Ease: " + str(Document.readability_flesch_re))
    print("Readability (SMOG): " + str(Document.readability_smog_index))
    print("Readability (ARI): " + str(Document.readability_ari))
    for word, frequency in #Document.freq_words:
    for word in Document.modal_dist:
        print word

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze Student Writing')
    parser.add_argument("filename", help="set path to file to analyze")
    parser.add_argument('-t', '--title', help="set the title of the document to be analyzed", action="store", type=str)
    parser.add_argument('-u', '--user', help="set the name of the current user", action="store", type=str)
    parser.add_argument('-v', '--verbose', help="detailed output", action="store_true")
    parser.add_argument('-w', '--writer', help="the author of the paper to be analyzed", action="store", type=str)
    args = parser.parse_args()

    # argparse test results
    if os.path.isfile(args.filename):
        filename = args.filename



    if args.title:
        doc_title = args.title

    if args.user:
        user = args.user


    if args.verbose:
        print "Path to file: " + args.filename


    main(filename)

    if args.user:
        print "User is: " + args.user
    if args.writer:
        print "Author: " + args.writer
