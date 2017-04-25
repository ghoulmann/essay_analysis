# -*- coding: utf-8 -*-

"""
Intended as the CLI entry point for the thing.
"""

import sys
import os
import argparse
from input import read_document as input

def main(path, *string):
    Document = input.Sample(path, string)
    print(Document.raw_text)
    print(Document.path)
    print(Document.author)
    print(Document.abs_path)
    #print(Document.be_verb_count)
    #print(str(Document.be_verb_ratio) + " %")

def usage():
    print "Requires path, 'author name'."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze Student Writing')
    parser.add_argument("-a", "--author", help="set writer's name", action="store_true", required=True)
    parser.add_argument("-p", "--path", help="set path to file to analyze", action="store_true", required=True)
    args = parser.parse_args()


    if len(sys.argv) == 3:
        if os.path.isfile(sys.argv[1]):
            main(sys.argv[1], str(sys.argv[2]))
        else:
            usage()
    else:
        usage()
