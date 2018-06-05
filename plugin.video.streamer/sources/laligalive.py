from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        knownbases = ['laliga-live.to']
        custom_iframe = re.compile('<iframe.+?class=[\'"]video[\'"].+?src=[\'"](.+?)[\'"]')
        resp = self.sess.get(link).content
        resolved = custom_iframe.findall(resp)[0]
        return resolved