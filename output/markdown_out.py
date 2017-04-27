import codecs
import tempfile

class MarkdownReport:
    def __init__(self):
        self.File = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix="", prefix=template, dir=markdown_report, delete=False)
