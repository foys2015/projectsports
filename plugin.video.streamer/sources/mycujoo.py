from .tools.common import Utils
import json
import re

class Scraper(Utils):
    def resolve(self, link):
        window = re.compile('window\.\_d\s+=\s+(\{.+?\});', re.DOTALL)
        
        stream_page = self.sess.get(link).content
        stream_jsonStr = window.findall(stream_page)[0]
        stream_jsonObj = json.loads(stream_jsonStr)
        
        resolved = '{stream}|Referer={referer}&User-Agent={useragent}'.format(stream=stream_jsonObj['video']['filename'],
                                                                              referer=link, useragent=self.ua)
        return resolved