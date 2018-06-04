from importlib import import_module
from ..thebeast import TheBeast
from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['laliga-live.to']
        self.testlink = 'laliga-live.to/watch/2018_Barcelona_Open_Day_Four_live_Tennis/stream7'
        self.tb = TheBeast()
        self.session = requests.Session()
        
    def resolve(self, link):
        
        custom_iframe = re.compile('<iframe.+?class=[\'"]video[\'"].+?src=[\'"](.+?)[\'"]')
        start_page = self.session.get(link).content
        resolved = custom_iframe.findall(start_page)[0]
        print 'laligalive.py: %s resolved to %s' % (link, resolved)
        ref = link
        vars = self.get_id(resolved, ref)
        if 'bro.adca.st' in vars[-1]:
            link = 'http://bro.adca.st/stream/%s.html' % vars[0]
            print 'laligalive.py: %s resolved to %s' % (vars[-1], link)
            #Make sure we're able to follow the iframe link
            self.session.headers.update({'Referer':vars[-1],'User-Agent':self.ua})
            ref = link
            page = self.session.get(link).content
            tamborRe = re.compile('tambor\s+=\s+["\'](.+?)["\'];\s+firme\s+=\s+["\'](.+?)["\'];')
            result = tamborRe.findall(page)[0]
            token = json.loads(requests.get('http://bro.adca.st'+result[1]).text)['rumba']
            final = result[0] + token + '|User-Agent=' + self.ua + '&Referer=' + ref
            print 'laligalive.py: %s resolved to %s' % (ref, result[0] + token)
            return final
        else:
            print 'laligalive.py: there\'s a host other than bro.adca.st - %s' % result[-1]
            return ''