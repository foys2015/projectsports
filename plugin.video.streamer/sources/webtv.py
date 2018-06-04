from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['webtv.ws']
        
    def resolve(self, link):
        resolved = self.get_source(link)
        print 'webtv.py: %s resolved to %s' % (link, resolved)
        return resolved