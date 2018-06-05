from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        script = re.compile('<script.+?src=["\'](?!.*googleapis)(\S{10,})["\']')
        targetAll = re.compile('target\.All\s*=\s*["\'](.+?)["\'];')
        resp = self.sess.get(link).content
        #First, make sure we're using the right domain/endpoint
        replaceWith = targetAll.findall(resp)[0]
        nextLink = link[:link.find('/vip')] + replaceWith
        #Update the session referer to be the current domain/endpoint
        #So we can move onto the correct domain/endpoint
        self.sess.headers.update({'Referer':link})
        resp = self.sess.get(nextLink).content
        resolved = self.script.findall(resp)[0]
        return resolved