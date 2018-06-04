from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['widestream.io']
        
    def resolve(self, link):
        resolved = self.get_file(link)
        print 'widestream.py: %s resolved to %s' % (link, resolved)
        return resolved