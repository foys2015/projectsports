from ..thebeast import RegExp
import requests
import json
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['bro.adca.st']
        self.base = 'http://bro.adca.st'
        self.tamborRe = re.compile('tambor\s+=\s+["\'](.+?)["\'];\s+firme\s+=\s+["\'](.+?)["\'];')
        
    def resolve(self, link, vars):
        ref = 'http://cricfree.sc/update/{channel}.php'.format(channel=vars[0])
        #Make sure we're able to follow the iframe link
        start = 'http://bro.adca.st/stream.php?id={0}&p=1&c=0&stretching=uniform&old=0'.format(id)
        resp = sess.get(start, headers={'Referer':ref})
        # Get the URL
        m = re.compile ('tambor = "(.*?)"').search(resp.content)
        streamPath = m.group(1)

        # Get the tokenpage
        m = re.compile ('firme = "(.*?)"').search(resp.content)
        tokenurl = m.group(1)
        tokenPage = sess.get('http://bro.adca.st' + tokenurl, headers={'Referer':start, 'X-Requested-With': 'XMLHttpRequest'})
        m = re.compile (':"(.*?)"').search(tokenPage.content)
        token = m.group(1)

        link = streamPath + token
        headerString = '|Referer={0}&User-Agent={1}&Origin=http://bro.adca.st'.format(urllib.quote(start, safe=''), ua)
        link += headerString
        
        return link