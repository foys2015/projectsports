from ..thebeast import RegExp
import requests
import base64
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['playcast.se']
        self.streamUrl = 'http://www.playcast.se/stream.php?id=%s'
        self.curlRe = re.compile('curl\s*=\s*[\'"](.+?)[\'"];')
        
    def resolve(self, link, vars):
        try:
            stream = self.streamUrl % vars[0]
            #ContentDecodingError: Fix found at https://github.com/requests/requests/issues/3849
            page = requests.get(stream, headers={'Referer': link, 'User-Agent': self.ua, 'Accept-Encoding': 'identity'}).content
            curl = self.curlRe.findall(page)[0]
            resolved = base64.b64decode(curl) + '|User-Agent=%s&Referer=%s' % (self.ua, stream)
            print 'playcast.py: link should now be resolved'
            return resolved
        except:
            print 'playcast.py: resolve function failed - %s' % stream
            return ''