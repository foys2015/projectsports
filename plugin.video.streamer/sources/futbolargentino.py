from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['futbolargentino.stream']
        
    def resolve(self, link):
        resolved = self.get_clappr(link)
        print 'futbolargentino.py: %s resolved to %s' % (link, resolved)
        return resolved