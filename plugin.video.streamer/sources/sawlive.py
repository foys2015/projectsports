from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        embed_link = 'http://www.sawlive.tv/embed/stream/{0}/{1}'
        params = re.compile('var \w*\s*=\s*["\'](.+?)["\']')
        resp = self.sess.get(link).content
        p = params.findall(resp)[0]
        stream = embed_link.format(p.split(';')[1], p.split(';')[0])
        #This logic is incorrect, link is not valid
        return stream