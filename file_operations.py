# -*- coding: utf-8 -*-
import os
from mimetypes import MimeTypes
from pdf_to_text import convert_pdf_to_txt as pdf_in
import docx_to_string
class FileOperations:
    def __init__(self, path):
        self.path = path
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(path)
            self.guessed_type = MimeTypes.mime.guess_type(self.path)
            self.file_type = self.guessed_type[0]
            if "text" in self.file_type:
                with open(self.path) as fobj:
                    self.raw_text = fobj.read()
            elif "pdf" in self.file_type:
                self.raw_text = pdf_in(self.path)
            elif "docx" in self.file_type:
                self.raw_text = get_docx_text(self.path)
            else:
                print(self.file_name + "is not a compatible document.")
