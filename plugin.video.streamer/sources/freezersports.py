from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['freezersports.com']
        self.testlink = 'freezersports.com/mlb/sx/mlb15.php'
        self.tb = TheBeast()
        
    def resolve(self, link):
        ref = link
        print ref
        resolved = self.get_iframe(link)
        ref = resolved
        print ref
        resolved = self.get_iframe(resolved)
        ref = resolved
        print ref
        resolved = self.get_iframe(resolved)
        return self.outsource(resolved)
            
    def outsource(self, link):
        
        original = link
        test = requests.get(link, allow_redirects=True)
        if test.history:
            #We were redirected
            #Check for final url as source
            link = test.url
            print link
        validSource = self.tb._validate(link)
        if validSource is not None:
            print 'sportlive.py: outsourcing resolving to %s' % validSource
            if not link.startswith('http'):
                link = 'http:' + link
            source = import_module('.'+validSource, package='thebeast.sources')
            if test.history: resolved = source.Site().resolve(original, link)
            else: resolved = source.Site().resolve(original)
            print 'sportlive.py: received resolved link from %s' % validSource
            return resolved
        else:
            print 'sportlive.py: link should already be resolved'
            return link