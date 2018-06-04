from HTMLParser import HTMLParser
from ..thebeast import RegExp
from urllib import unquote
import requests
import base64
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['cricfree.cc']
        self.sequence = ['iframe','packer','clappr']
        self.parser = HTMLParser()
        
    def resolve(self, link):
        listRe = re.compile('var\s+\w{3}\s+=\s+(\[.+?\]);', re.DOTALL)
        minusRe = re.compile('\s+\-\s+(\d{,10})\);')
        
        page = requests.get(link).content
        
        jsList = listRe.findall(page)[0]
        minusValue = int(minusRe.findall(page)[0])
        valuesList = eval(jsList)
        
        iframePage = self.parser.unescape(unquote(''.join(map(chr,
                                          [int(''.join([x for x in
                                          base64.b64decode(valueInList)
                                          if x.isdigit()])) - minusValue
                                          for valueInList in valuesList]))))
        #We have to use iframe regexp here directly
        #because we had to decode the page contents first
        iframe_url = self.iframe.findall(iframePage)[0]
        unpacked = self.get_packer(iframe_url, ref=link)
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