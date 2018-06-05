from .tools.common import Utils
import re

class Scraper(Utils):
    def resolve(self, link):
        vars = re.compile('width=(\d{3}),\s*height=(\d{3}),\s*channel=[\'"](.+?)[\'"],\s*g=[\'"](.+?)[\'"];')
        js = re.compile('<script type=[\'"]text\/javascript[\'"].+?src=[\'"](.+?)[\'"]')
        page = self.sess.get(link).content
        nextLink = js.findall(page)[0]
        pageVars = vars.findall(page)[0]
        #We need to get link using player.js & id variables
        return 'Nothing for now'