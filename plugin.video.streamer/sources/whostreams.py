from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['whostreams.net']
        
    def resolve(self, link):
        ref = link
        unpacked = self.get_packer(link)
        resolved = self.get_clappr(unpacked)
        print 'whostreams.py: %s resolved to %s' % (link, resolved)
        resolved += '|User-Agent=%s&Referer=%s' % (self.ua, link)
        return resolved