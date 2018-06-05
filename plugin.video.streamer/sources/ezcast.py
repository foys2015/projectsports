from .tools.common import Utils
import re

class Site(Utils):
    def resolve(self, link):
        knownbases = ['embedezcast.com','ezcast.tv']
        ajaxRe = re.compile('source\.setAttribute\([\'"]src[\'"],\s*[\'"](.+?)[\'"].+?[\'"](.+?)[\'"]\);.+?\$\.ajax\(\{url:\s*[\'"](.+?)[\'"]', re.DOTALL)
        playerUrl = 'http://www.embedezcast.com/membedplayer/{channel}/{g}/{width}/{height}'
        
        #This needs to be redone
        player = playerUrl.format(channel=vars[2], g=vars[3], width=vars[0], height=vars[1])
        self.sess.headers.update({'Referer':link})
        page = self.sess.get(player).content
        result = ajaxRe.findall(page)[0]
        r = result[2]
        if r.endswith('?'): r = r[:-2]
        ajax_base = self.sess.get(r).text.split('=')[1]
        
        resolved = result[0] + ajax_base + result[1] + '|User-Agent=%s&Referer=%s' % (self.ua, player)
        return resolved