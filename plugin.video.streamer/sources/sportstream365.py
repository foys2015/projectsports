import requests
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    session.headers.update({'If-Modified-Since':'Sat, 1 Jan 2000 00:00:00 GMT'})
    serverIP = session.post('http://sport-stream365.com/cinema').text
    gameId = re.compile('game=(.+?)&').findall(link)[0]
    final = 'http://{ip}/hls-live/xmlive/_definst_/{gameId1}/{gameId2}.m3u8|User-Agent={useragent}&Referer={referer}'
    resolved = final.format(ip=serverIP, gameId1=gameId, gameId2=gameId, useragent=uAgent, referer=link)
    
    return resolved