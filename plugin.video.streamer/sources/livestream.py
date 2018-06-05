from .tools.common import Utils
import json
import re

class Scraper(Utils):
    def resolve(self, link):
        window = re.compile('window\.config\s+=\s+(\{.+?\});</script>', re.DOTALL)
        
        stream_page = self.sess.get(link).content
        stream_jsonStr = window.findall(stream_page)[0]
        jsonObj = json.loads(stream_jsonStr)
        
        resolved = '{stream}|Referer={referer}&User-Agent={useragent}'.format(stream=json_obj['event']['stream_info']['m3u8_url'],
                                                                              referer=link, useragent=self.ua)
        return resolved