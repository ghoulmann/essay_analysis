"""This script contains a function that makes an API call to
http://text-processing.com/api/sentiment/ and hopes to return the "label"
field.
"""
import sys
import requests
def fetch(passage):
    url = "http://text-processing.com/api/sentiment/"
    print url
    print passage
    print raw_text
    r = requests.post(url, data="text=" + passage)
    print r
    for x,y in r:
        if x = "label":
            print y



sentiment_result = fetch("I love to hate.")
if sentiment_result:
    print sentiment_result
    sentiment = sentiment_result["label"]
    print sentiment
