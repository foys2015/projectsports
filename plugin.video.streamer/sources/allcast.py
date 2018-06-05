from .tools.common import Utils

class Scraper(Utils):
    def resolve(self, link):
        resp = self.sess.get(link).content
        try:
            iframeLink = self.iframe.findall(resp)[0]
            self.sess.headers.update({'Referer':link})
            resp = self.sess.get(iframeLink).content
            vars = self.id.findall(resp)[0]
        except:
            vars = self.id.findall(resp)[0]
        #Get js using js function from common
        return 'Returning Nothing for now'