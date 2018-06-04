from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['ok.nowlive.pw']
        
    def resolve(self, link, ref=None):
        if ref: resolved = self.get_source(link, ref)
        else: resolved = self.get_source(link)
        print 'nowlive.py: %s resolved to %s' % (link, resolved)
        return resolved