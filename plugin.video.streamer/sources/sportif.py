from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['sportif.pw']
        self.testlink = 'sportif.pw/webgo.php?v=215&f=2'
        self.tb = TheBeast()
        
    def resolve(self, link):
        resolved = self.get_iframe(link)
        print 'sportif.py: %s resolved to %s' % (link, resolved)
        
        #Link is usually whostreams,
        #so we can call its resolver to do the work
        validSource = self.tb._validate(resolved)
        if validSource is not None:
            if not resolved.startswith('http'):
                link = 'http:' + resolved
            else: 
                link = resolved
            source = import_module('.'+validSource, package='thebeast.sources')
            resolved = source.Site().resolve(link)
            print 'sportif.py: %s resolved to %s' % (link, resolved)
            return resolved
        else:
            print 'sportif.py: resolve function failed with link %s' % link