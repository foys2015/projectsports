from .tools.common import Utils
from .tools import jsunpack
import base64
import urllib
import json
import re

class Scraper(Utils):
    def resolve(self, link):
        telerium = re.compile('"\s*\W(\w{10})\W*(.+?)[\'"];\W*\w{10}\s*=\s*".*?";\W*(\w{10})\W*(.+?)[\'"];', re.DOTALL)
        
        firstPage = self.sess.get(link).content
        secondLink = self.iframe.findall(firstPage)[0]
        self.sess.headers.update({'Referer':link})
        secondPage = self.sess.get(secondLink).content
        thirdLink = self.iframe.findall(secondPage)[0]
        self.sess.headers.update({'Referer':secondLink})
        thirdPage = self.sess.get(thirdLink).content
        try:
            vars = telerium.findall(thirdPage)[0]
            
            tBase = 'http://telerium.tv'
            tokenPage = tBase + base64.b64decode(vars[-1])
            tokenPage = self.sess.get(tokenPage, headers={'Referer':thirdLink, 'X-Requested-With': 'XMLHttpRequest'})
            m = re.compile(':"(.*?)"').search(tokenPage.content)
            tok = m.group(1)
            
            start = urllib.quote(thirdLink, safe='')
            
            base = base64.b64decode(vars[1])
            before = re.compile('sf=(\w*==)').findall(base)[0]
            after = base64.b64decode(before)
            base = base.replace(before, after)
            stream = '{base}{token}|'.format(base=base, token=tok) + \
                     'Referer={ref}&User-Agent={useragent}&Origin=http://telerium.tv/'.format(ref=start, useragent=self.ua)
            #This stream still returns 403, so must be doing somethign wrong
        except:
            packed = self.packer.findall(thirdPage)[0]
            from tools import jsunpack
            unpacked = jsunpack.unpack(packed)
            stream = self.clappr.findall(unpacked)[0]
        return stream