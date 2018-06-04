from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['sportlive.site']
        self.session = requests.Session()
        self.testlink = 'sportlive.site/vip1/arenahr1.php'
        self.tb = TheBeast()
        
    def resolve(self, link):
        #try:
        ref = link
        resolved = self.get_iframe(link)
        result = self.get_id(resolved)
        return self.outsource(result[-1], result)
            
    def outsource(self, link, vars=None):
        validSource = self.tb._validate(link)
        if validSource is not None:
            print 'sportlive.py: outsourcing resolving to %s' % validSource
            if not link.startswith('http'):
                link = 'http:' + link
            source = import_module('.'+validSource, package='thebeast.sources')
            if vars: resolved = source.Site().resolve(link, vars)
            else: resolved = source.Site().resolve(link)
            print 'sportlive.py: received resolved link from %s' % validSource
            return resolved
        else:
            print 'sportlive.py: link should already be resolved'
            return link