from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        videolink = re.compile('var\s+videoLink\s*=\s*[\'"](.+?)[\'"];')
        stream_page = self.sess.get(link).content
        stream = videolink.findall(stream_page)[0]
        return stream