from .tools.common import Utils
import base64
import re

class Scraper(Utils):
    def resolve(self, link):
        #Starting url needs to be like the one below
        streamUrl = 'http://www.playcast.se/stream.php?id=%s'
        curlRe = re.compile('curl\s*=\s*[\'"](.+?)[\'"];')
        
        #ContentDecodingError: Fix found at https://github.com/requests/requests/issues/3849
        self.sess.headers.update({'Accept-Encoding': 'identity'})
        page = self.sess.get(link).content
        curl = curlRe.findall(page)[0]
        resolved = base64.b64decode(curl) + '|User-Agent=%s&Referer=%s' % (self.ua, link)
        return resolved