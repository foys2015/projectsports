from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['daddylive.info']
        self.testlink = 'daddylive.info/livetv/arenasport3serbiaclap.php'
        self.tb = TheBeast()
        
    def resolve(self, link):
        resolved = self.get_iframe(link)
        print 'daddylive.py: %s resolved to %s' % (link, resolved)
        
        #Link is usually whostreams,
        #so we can call its resolver to do the work
        validSource = self.tb._validate(resolved)
        if validSource is not None:
            print 'daddylive.py: outsourcing resolving of %s to %s' % (resolved, validSource)
            if not resolved.startswith('http'):
                link = 'http:' + resolved
            else: 
                link = resolved
            source = import_module('.'+validSource, package='thebeast.sources')
            resolved = source.Site().resolve(link)
            print 'daddylive.py: %s resolved to %s' % (link, resolved)
            return resolved
        else:
            print 'daddylive.py: resolve function failed with link %s' % link
            return ''