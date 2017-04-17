import markdown
import codecs
import webbrowser
import os
import time
input_file = codecs.open("/tmp/report.md", "r")
text = input_file.read()
html = markdown.markdown(text)

output_file = codecs.open("output/report.html"
    , "w",
    encoding="utf-8",
    errors="xmlcarrefreplace"
    )
output_file.write(html)
webbrowser.open("output/report.html")
#time.sleep(10)
#os.remove("output/report.html")
