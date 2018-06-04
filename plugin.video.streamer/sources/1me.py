import requests
import base64
import urllib
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    iframe = re.compile('<iframe.+?src=[\'"](.+?)[\'"]')
    telerium = re.compile('"\s*\W(\w{10})\W*(.+?)[\'"];\W*\w{10}\s*=\s*".*?";\W*(\w{10})\W*(.+?)[\'"];', re.DOTALL)
    packer = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
    clappr = re.compile('new\s+Clappr\.Player\(\{\s*?source:\s*?["\'](.+?)["\']')
    
    firstPage = session.get(link).content
    secondLink = iframe.findall(firstPage)[0]
    session.headers.update({'Referer':link})
    secondPage = session.get(secondLink).content
    thirdLink = iframe.findall(secondPage)[0]
    session.headers.update({'Referer':secondLink})
    thirdPage = session.get(thirdLink).content
    try:
        vars = telerium.findall(thirdPage)[0]
        
        tBase = 'http://telerium.tv'
        tokenPage = tBase + base64.b64decode(vars[-1])
        tokenPage = session.get(tokenPage, headers={'Referer':thirdLink, 'X-Requested-With': 'XMLHttpRequest'})
        m = re.compile (':"(.*?)"').search(tokenPage.content)
        tok = m.group(1)
        
        start = urllib.quote(thirdLink, safe='')
        
        base = base64.b64decode(vars[1])
        before = re.compile('sf=(\w*==)').findall(base)[0]
        after = base64.b64decode(before)
        base = base.replace(before, after)
        stream = '{base}{token}|'.format(base=base, token=tok) + \
                 'Referer={ref}&User-Agent={useragent}&Origin=http://telerium.tv/'.format(ref=start, useragent=uAgent)
        #This stream still returns 403, so must be doing somethign wrong
    except:
        packed = packer.findall(thirdPage)[0]
        from tools import jsunpack
        unpacked = jsunpack.unpack(packed)
        stream = clappr.findall(unpacked)[0]
    return stream