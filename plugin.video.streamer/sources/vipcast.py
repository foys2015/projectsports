from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['vipcast.pw']
        self.tb = TheBeast()
        
    def resolve(self, link):
        resolved = self.get_iframe(link)
        return self.outsource(resolved)
        
    def outsource(self, link):
        validSource = self.tb._validate(link)
        if validSource is not None:
            print 'vipcast.py: outsourcing resolving to %s' % validSource
            if not link.startswith('http'):
                link = 'http:' + link
            source = import_module('.'+validSource, package='thebeast.sources')
            resolved = source.Site().resolve(link)
            print 'vipcast.py: received resolved link from %s' % validSource
            return resolved
        else:
            print 'vipcast.py: link should already be resolved'
            return link