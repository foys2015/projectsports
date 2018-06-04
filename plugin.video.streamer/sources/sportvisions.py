import requests
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    serverUrl = re.compile('var\s+servers\s*?=\s*?[\'"](.+?)[\'"];')
    js = 'http://sportvisions.ws/js/config-stream.js'
    
    c = link.split('/')[-1]
    page = session.get(js).content
    server_url = serverUrl.findall(page)[0]
    server_ip = json.loads(session.get(server_url).text)['data']['url']
    
    resolved = 'http://{base}/channels/{channel}/stream.m3u8|'.format(base=server_ip, channel=c) + \
               'Referer={referer}&User-Agent={useragent}'.format(referer=link, useragent=uAgent)
    
    return resolved