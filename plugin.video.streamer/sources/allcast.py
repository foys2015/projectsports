from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['allcast.is']
        self.tb = TheBeast()
        
    def resolve(self, link):
        #try:
        ref = link
        result = self.get_id(link)
        if len(result) == 0:
            result = self.get_iframe(link)
            return self.outsource(result)
        else:
            return self.outsource(result[-1], result)
        """
        except:
            print 'allcast.py: resolve function failed with link %s' % link
            return ''
        """
            
    def outsource(self, link, vars=None):
        validSource = self.tb._validate(link)
        if validSource is not None:
            print 'allcast.py: outsourcing resolving to %s' % validSource
            if not link.startswith('http'):
                link = 'http:' + link
            source = import_module('.'+validSource, package='thebeast.sources')
            if vars: resolved = source.Site().resolve(link, vars)
            else: resolved = source.Site().resolve(link)
            print 'allcast.py: received resolved link from %s' % validSource
            return resolved
        else:
            print 'allcast.py: link should already be resolved'
            return link