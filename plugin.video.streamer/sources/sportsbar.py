from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        videoLinkRe = re.compile('var\s+videoLink\s+=\s+[\'"](.+?)[\'"];')
        page = self.sess.get(link).content
        #skip rtmp url, opt for https url
        end_url = videoLinkRe.findall(page)[0]
        resolved = '{url}|Referer={referer}&User-Agent={useragent}'.format(url=end_url, referer=link, useragent=self.ua)
        return resolved