from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['nominasport.eu']
        self.testlink = 'nominasport.eu/ana24/hdsport1pt.html'
        self.tb = TheBeast()
        
    def resolve(self, link):
        link = link.strip().rstrip()
        resolved = self.get_iframe(link)
        
        #Site usually goes 2 links deep
        resolved = self.get_iframe(resolved, link)
        #prevent module from calling itself
        if resolved != link:
            #Now we outsource
            self.outsource(resolved)
        
    def outsource(self, link, vars=None):
        validSource = self.tb._validate(link)
        if validSource is not None:
            print 'nominasport.py: outsourcing resolving to %s' % validSource
            if not link.startswith('http'):
                link = 'http:' + link
            source = import_module('.'+validSource, package='thebeast.sources')
            if vars: resolved = source.Site().resolve(link, vars)
            else: resolved = source.Site().resolve(link)
            print 'nominasport.py: received resolved link from %s' % validSource
            return resolved
        else:
            print 'nominasport.py: link should already be resolved'
            return link