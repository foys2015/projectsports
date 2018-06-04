import requests
import base64
import urllib
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    session.headers.update({'User-Agent':uAgent})
    embed_link = 'http://www.sawlive.tv/embed/stream/{0}/{1}'
    params = re.compile('var \w*\s*=\s*["\'](.+?)["\']')
    resp = session.get(link).content
    p = params.findall(resp)[0]
    stream = embed_link.format(p.split(';')[1], p.split(';')[0])
    #This logic is incorrect, link is not valid
    return stream