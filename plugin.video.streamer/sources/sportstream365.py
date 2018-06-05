from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        self.sess.headers.update({'If-Modified-Since':'Sat, 1 Jan 2000 00:00:00 GMT'})
        serverIP = self.sess.post('http://sport-stream365.com/cinema').text
        gameId = re.compile('game=(.+?)&').findall(link)[0]
        final = 'http://{ip}/hls-live/xmlive/_definst_/{gameId1}/{gameId2}.m3u8|User-Agent={useragent}&Referer={referer}'
        resolved = final.format(ip=serverIP, gameId1=gameId, gameId2=gameId, useragent=self.ua, referer=link)
        return resolved