# -*- coding: utf-8 -*-

"""
Intended as the CLI entry point for the thing.
"""

import sys
import os
import argparse
from input import read_document as input

def main(path, *author):
    Document = input.Sample(path, author)
    print("Base Name: " + Document.file_name)
    print("Relative path to file: " + Document.path)
    print("Author: " + str(Document.author))
    print("Absolute path to file: " + Document.abs_path)
    print("Weak Verbs to Sentences: " + str(Document.weak_verbs_to_sentences))
    print("Weak verb count: " + str(Document.be_verb_count))
    print("Percent passive sentences: " + str(Document.percent_passive) + " %")
    print("Sentence Count: " + str(Document.sentence_count))
    print("Example passive sentence from document: " + Document.passive_sentences[-1])
    print("Example weak-verb usage: " + Document.weak_sentences_all[-2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze Student Writing')
    parser.add_argument("filename", help="set path to file to analyze")
    parser.add_argument('-a', '--author', help="set writer's name", action="store", type=str, nargs='?')
    parser.add_argument('-v', '--verbose', help="verbose output", action="store_true")
    args = parser.parse_args()
    """
    .. todo:: add arguments for doc title and teacher name
    """


    if os.path.isfile(args.filename):
        filename = args.filename

    if args.author:
        author = str(args.author)
    else:
        author = ""

    if args.verbose:
        print "Path to file: " + args.filename
        print "Author: " + args.author


    main(filename, author)
