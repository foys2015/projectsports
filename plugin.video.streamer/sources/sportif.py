from .tools.common import Utils

class Scraper(Utils):
    def resolve(self, link):
        stream_page = self.sess.get(link).content
        resolved = self.iframe.findall(stream_page)[0]
        return resolved