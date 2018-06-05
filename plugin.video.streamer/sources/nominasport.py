from .tools.common import Utils
import json
import re

class Scraper(Utils):
    def resolve(self, link):
        link = link.strip().rstrip()
        resp = self.sess.get(link).content
        resolved = self.iframe.findall(resp)[0]
        return resolved