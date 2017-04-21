# -*- coding: utf-8 -*-

"""
Intended as the CLI entry point for the thing.
"""

import sys
import document_in

def main(path, *string):
    Document = document_in.Document(path, string)
    print(Document.path)
    print(Document.author)

def usage():
    print "Requires path, 'author name'."

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        usage()
