from HTMLParser import HTMLParser
from .tools.common import Utils
from .tools import jsunpack
from urllib import unquote
import base64
import re

class Scraper(Utils):
    def resolve(self, link):
        parser = HTMLParser()
        listRe = re.compile('var\s+\w{3}\s+=\s+(\[.+?\]);', re.DOTALL)
        minusRe = re.compile('\s+\-\s+(\d{,10})\);')
        
        page = self.sess.get(link).content
        
        jsList = listRe.findall(page)[0]
        minusValue = int(minusRe.findall(page)[0])
        valuesList = eval(jsList)
        
        iframePage = parser.unescape(unquote(''.join(map(chr,
                                    [int(''.join([x for x in
                                    base64.b64decode(valueInList)
                                    if x.isdigit()])) - minusValue
                                    for valueInList in valuesList]))))
        #We have to use iframe regexp here directly
        #because we had to decode the page contents first
        iframe_url = self.iframe.findall(iframePage)[0]
        self.sess.headers.update({'Referer':link})
        resp = self.sess.get(iframe_url).content
        unpacked = jsunpack.unpack(resp)
        if unpacked == '':
            print 'cricfree.py: No packer code found'
            return ''
        else:
            try:
                clapprStream = self.clappr.findall(unpacked)[0]
                headers = '|Referer=%s&User-Agent=%s' % (iframe_url, self.ua)
                return clapprStream + headers
            except:
                print 'cricfree.py: No clappr code found'
                print 'unpacked packer code is as follows'
                print unpacked
                return ''