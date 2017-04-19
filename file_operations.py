# -*- coding: utf-8 -*-
import os

class FileOperations:
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        with open(self.path) as fobj:
            self.raw_text = fobj.read()
