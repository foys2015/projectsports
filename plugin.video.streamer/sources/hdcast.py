from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        js_re = re.compile('function\s+[a-zA-Z]{,15}\(\)\s+\{\s+return\(\[(.+?)\]\.join\(""\)\)')
        resp = self.sess.get(link).content
        #skip rtmp url, opt for https url
        stream_link = js_re.findall(resp)[1]
        end_url = stream_link.replace('"','').replace(',','').replace('\/','/')
        resolved = '{url}|Referer={referer}&User-Agent={useragent}'.format(url=end_url, link, self.ua)
        return resolved