from .tools.common import Utils

class Scraper(Utils):
    def resolve(self, link):
        resp = self.sess.get(link).content
        resolved = self.iframe.findall(resp)[0]
        self.sess.headers.update({'Referer':link})
        resp = self.sess.get(resolved).content
        vars = self.id.findall(resp)[0]
        #We need to get link using player.js & id variables
        return 'Nothing for now'