# -*- coding: utf-8 -*-

import sys
import document_in

def main(path, *string):
    Document = document_in.FileOperations(path, string)
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
