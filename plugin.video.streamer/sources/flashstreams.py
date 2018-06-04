from urlparse import urlparse
import requests
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    iframe = re.compile('<iframe.+?src=[\'"](.+?)[\'"]')
    file = re.compile('[\{,\s].*?file:.*?[\'"](.+?)[\'"]')
    
    page = session.get(link).content
    nextLink = iframe.findall(page)[0]
    
    if 'widestream' in nextLink:
        parsed = urlparse(nextLink)
        o = '{0}://{1}{2}'.format(parsed.scheme, parsed.netloc, parsed.path)
        session.headers.update({'Referer':link, 'User-Agent': uAgent})
        nextPage = session.get(nextLink).content
        link = file.findall(nextPage)[0]
    
    
        resolved = '{url}|Origin={origin}&Referer={referer}&User-Agent{useragent}'.format(url=link, origin=o, 
                                                                                          referer=nextLink, 
                                                                                          useragent=uAgent)
        
        return resolved