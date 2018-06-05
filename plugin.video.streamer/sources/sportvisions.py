from .tools.common import Utils
import json
import re

class Scraper(Utils):
    def resolve(self, link):
        serverUrl = re.compile('var\s+servers\s*?=\s*?[\'"](.+?)[\'"];')
        js = 'http://sportvisions.ws/js/config-stream.js'
        
        c = link.split('/')[-1]
        page = self.sess.get(js).content
        server_url = serverUrl.findall(page)[0]
        server_ip = json.loads(self.sess.get(server_url).text)['data']['url']
        
        resolved = 'http://{base}/channels/{channel}/stream.m3u8|'.format(base=server_ip, channel=c) + \
                   'Referer={referer}&User-Agent={useragent}'.format(referer=link, useragent=self.ua)
        return resolved