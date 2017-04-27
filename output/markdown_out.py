import codecs
import tempfile

class MarkdownReport:
    def __init__(self):
        self.filename = self.file_out.name

    def file_out(self):
        output = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix="", prefix=template, dir=None, delete=False)
        return output
