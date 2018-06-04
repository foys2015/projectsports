import requests
import urllib
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    source = re.compile('src=[\'"](.+?)[\'"]')
    
    firstPage = session.get(link).content
    secondLink = source.findall(firstPage)[0]
    secondPage = session.get(secondLink).content
    thirdLink = source.findall(secondPage)[0]
    thirdPage = session.get(thirdLink).content

    vars = re.compile('>.*?id=[\'"](.+?)[\'"].+?</script><script type=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]').findall(thirdPage)[0]
    if 'telerium' in vars[1]:
    
        start = 'http://telerium.tv/stream.php?id={0}&p=1&c=0&stretching=uniform&old=0'.format(id)
        resp = sess.get(start, headers={'Referer':ref})
        # Get the URL
        m = re.compile ('tambor = "(.*?)"').search(resp.content)
        streamPath = m.group(1)

        # Get the tokenpage
        m = re.compile ('firme = "(.*?)"').search(resp.content)
        tokenurl = m.group(1)
        tokenPage = sess.get('http://telerium.tv' + tokenurl, headers={'Referer':start, 'X-Requested-With': 'XMLHttpRequest'})
        m = re.compile (':"(.*?)"').search(tokenPage.content)
        token = m.group(1)

        link = streamPath + token
        headerString = '|Referer={0}&User-Agent={1}&Origin=http://telerium.tv'.format(urllib.quote(start, safe=''), ua)
        link += headerString
        return link