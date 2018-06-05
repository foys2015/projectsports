from .tools.common import Utils

class Scraper(Utils):
    def resolve(self, link):
        resp = self.sess.get(link).content
        nextLink = self.packer.findall(resp)[0]
        self.sess.headers.update({'Referer':link})
        nextResp = self.sess.get(nextLink).content
        resolved = self.clappr.findall(nextResp)[0]
        resolved = '{url}|User-Agent={useragent}&Referer={referer}'.format(url=resolved, useragent=self.ua, referer=nextLink)
        return resolved