from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['hdcast.pw']
        
    def resolve(self, link):
        js_re = re.compile('function\s+[a-zA-Z]{,15}\(\)\s+\{\s+return\(\[(.+?)\]\.join\(""\)\)')
        
        ref = link
        page = requests.get(link).content
        try:
            #skip rtmp url, opt for https url
            stream_link = js_re.findall(page)[1]
            end_url = stream_link.replace('"','').replace(',','').replace('\/','/')
            resolved = end_url + '|Referer=%s&User-Agent=%s' % (ref, self.ua)
            print 'hdcast.py: %s resolved to %s' % (ref, end_url)
            return resolved
        except:
            print 'hdcast.py: resolve function failed with link %s' % link
            return ''