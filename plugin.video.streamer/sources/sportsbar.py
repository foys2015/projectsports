from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['sportsbar.pw']
        
    def resolve(self, link):
        videoLinkRe = re.compile('var\s+videoLink\s+=\s+[\'"](.+?)[\'"];')
        
        ref = link
        page = requests.get(link).content
        try:
            #skip rtmp url, opt for https url
            end_url = videoLinkRe.findall(page)[0]
            resolved = end_url + '|Referer=%s&User-Agent=%s' % (ref, self.ua)
            print 'sportsbar.py: %s resolved to %s' % (ref, end_url)
            return resolved
        except:
            print 'sportsbar.py: resolve function failed with link %s' % link
            return ''