import requests
import urllib
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    iframe = re.compile('<iframe.+?src=[\'"](.+?)[\'"]')
    
    stream_page = session.get(link).content
    resolved = iframe.findall(stream_page)[-1]
    
    return resolved