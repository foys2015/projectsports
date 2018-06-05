from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        source = re.compile('src=[\'"](.+?)[\'"]')
        stream_page = self.sess.get(link).content
        resolved = source.findall(stream_page)[-1]
        return resolved