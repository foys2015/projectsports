from .tools.common import Utils

class Scraper(Utils):    
    def resolve(self, link):
        resp = self.sess.get(link).content
        resolved = self.iframe.findall(resp)[0]