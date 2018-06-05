from .tools.common import Utils

class Scraper(Utils):
    def resolve(self, link):
        resp = self.sess.get(link).content
        resolved = self.file.findall(resp)[0]
        return resolved