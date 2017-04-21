# -*- coding: utf-8 -*-
import os, sys
from mimetypes import MimeTypes

# docx method

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

# pdf method

from subprocess import Popen, PIPE
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

class Document:
    def __init__(self, path, *author):
        self.path = path
        self.author = author
        if os.path.isfile(self.path):
            self.file_name = os.path.basename(path)
            self.mime = MimeTypes()
            self.guessed_type = self.mime.guess_type(self.path)
            self.file_type = self.guessed_type[0]
            self.raw_text = self.get_raw_text(self, self.path, self.file_type)



    def get_raw_text(self, path, file_name, file_type):
        if "text" in self.file_type:
            with open(self.path) as fobj:
                raw_text = fobj.read()
        elif "pdf" in self.file_type:
            raw_text = self.pdf_to_text(self.path)
        elif "officedocument" in self.file_type:
            raw_text = self.docx_to_text(self.path)
        else:
            sys.exit()
        return raw_text

    def docx_to_text(self, path):
        """
        Take the path of a docx file as argument, return the text in unicode.
        """

        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'


        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = XML(xml_content)

        paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text
                     for node in paragraph.getiterator(TEXT)
                     if node.text]
            if texts:
                paragraphs.append(''.join(texts))

        raw_text = '\n\n'.join(paragraphs)
        return raw_text

    def pdf_to_text(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str