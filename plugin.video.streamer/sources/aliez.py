from .tools.common import Utils
import urllib

class Scraper(Utils):
    def resolve(self, link):
        stream_page = self.sess.get(link).content
        stream = self.file.findall(stream_page)[-1]
        resolved = urllib.unquote(stream)
        return resolved