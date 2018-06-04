from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['livesport4u.com']
        self.session = requests.Session()
        self.testlink = 'http://livesport4u.com/vip1/arenahr1-1.html'
        self.targetAll = re.compile('target\.All\s*=\s*["\'](.+?)["\'];')
        self.script = re.compile('<script.+?src=["\'](?!.*googleapis)(\S{10,})["\']')
        self.tb = TheBeast()
        
    def resolve(self, link):
        ref = link
        page = self.session.get(link).content
        #First, make sure we're using the right domain/endpoint
        replaceWith = self.targetAll.findall(page)[0]
        link = link[:link.find('/vip')] + replaceWith
        #Update the session referer to be the current domain/endpoint
        #So we can move onto the correct domain/endpoint
        self.session.headers.update({'Referer':ref})
        page = self.session.get(link).content
        resolved = self.script.findall(page)[0]
        
        validSource = self.tb._validate(resolved)
        if validSource is not None:
            print 'livesport4u.py: outsourcing resolving of %s to %s' % (resolved, validSource)
            if not resolved.startswith('http'):
                link = 'http:' + resolved
            else: 
                link = resolved
            source = import_module('.'+validSource, package='thebeast.sources')
            resolved = source.Site().resolve(link)
            print 'livesport4u.py: received resolved link %s from %s resolver' % (resolved, validSource)
            return resolved
        else:
            print 'livesport4u.py: resolve function failed with link %s' % link
            return resolved
        