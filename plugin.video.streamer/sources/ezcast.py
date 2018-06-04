from ..thebeast import RegExp
import requests
import re

class Site(RegExp):
    def __init__(self):
        RegExp.__init__(self)
        self.knownbases = ['embedezcast.com','ezcast.tv']
        self.ajaxRe = re.compile('source\.setAttribute\([\'"]src[\'"],\s*[\'"](.+?)[\'"].+?[\'"](.+?)[\'"]\);.+?\$\.ajax\(\{url:\s*[\'"](.+?)[\'"]', re.DOTALL)
        self.playerUrl = 'http://www.embedezcast.com/membedplayer/{channel}/{g}/{width}/{height}'
        
    def resolve(self, link, vars):
        try:
            player = self.playerUrl.format(channel=vars[2], g=vars[3], width=vars[0], height=vars[1])
            
            page = requests.get(player, headers={'Referer': link, 'User-Agent': self.ua}).content
            result = self.ajaxRe.findall(page)[0]
            r = result[2]
            if r.endswith('?'): r = r[:-2]
            ajax_base = requests.get(r).text.split('=')[1]
            
            resolved = result[0] + ajax_base + result[1] + '|User-Agent=%s&Referer=%s' % (self.ua, player)
            print 'ezcast.py: link should now be resolved'
            return resolved
        except:
            print 'ezcast.py: resolve function failed - %s' % link
            return ''