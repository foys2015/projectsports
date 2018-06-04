import requests
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    vars = re.compile('width=(\d{3}),\s*height=(\d{3}),\s*channel=[\'"](.+?)[\'"],\s*g=[\'"](.+?)[\'"];')
    js = re.compile('<script type=[\'"]text\/javascript[\'"].+?src=[\'"](.+?)[\'"]')
    loadbalancer = re.compile('\$\.ajax\(\{\s*url\s*:\s*[\'"](.+?)[\'"]')
    source = re.compile('setAttribute\([\'"]src[\'"],\s*[\'"](.+?)[\'"]\s*\+\s*\w{2}\s*\+\s*[\'"](.+?)[\'"]')
    
    page = session.get(link).content
    nextLink = js.findall(page)[0]
    pageVars = vars.findall(page)[0]
    if 'ucasterplayer' in nextLink:
        nextLink = 'http://www.ucasterplayer.com/membedplayer/' + \
                   '{channel}/{g}/{width}/{height}'.format(channel=pageVars[2], g=pageVars[3],
                                                           width=pageVars[0], height=pageVars[1])
        session.headers.update({'Referer':link})
        nextPage = session.get(nextLink).content
        lbLink = loadbalancer.findall(nextPage)[0]
        src = source.findall(nextPage)[0]
        server = session.get(lbLink).text.split('=')[1]
        
        resolved = '{0}{1}{2}'.format(source[0], server, source[1]) + \
                   '|Referer={referer}&User-Agent={useragent}'.format(referer=nextLink, useragent=uAgent)
        
        return resolved