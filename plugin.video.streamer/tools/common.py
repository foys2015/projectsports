# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from urlparse import urlparse
from urllib import unquote
import jsunpack
import requests
import base64
import json
import re

class Utils:
    def __init__(self):
        self.iframe = re.compile('<iframe.+?(?!.*</script)src=["\']\s*(?!.*urldelivery)(\S{10,})["\']')
        self.id = re.compile('>.*?id=[\'"](.+?)[\'"];\swidth=[\'"](.+?)[\'"];\sheight=[\'"](.+?)[\'"];</script><script type=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]')
        self.fid = re.compile('>.*?fid=[\'"](.+?)[\'"];\s+v\_width=(.+?);\s+v\_height=(.+?);</script><script.+?src=[\'"](.+?)[\'"]')
        self.source = re.compile('source(?:\:\s*|.+?src=)[\'"](.+?)[\'"]')
        self.file = re.compile('[\{,\s].*?file:.*?[\'"](.+?)[\'"]')
        self.clappr = re.compile('new\s+Clappr\.Player\(\{\s*?source:\s*?["\'](.+?)["\']')
        self.packer = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
        self.c = re.compile('>.*?id=[\'"](.+?)[\'"];\swidth=[\'"](.+?)[\'"];\sheight=[\'"](.+?)[\'"];\sc=[\'"](.+?)[\'"];</script><script type=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]')
        self.g = re.compile('>.*?width=(.+?),\sheight=(.+?),\schannel=[\'"](.+?)[\'"],\sg=[\'"](.+?)[\'"];</script><script type=[\'"]text/javascript[\'"]\ssrc=[\'"](.+?)[\'"]')
        
        self.ua = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/65.0.3325.181 Safari/537.36')
        self.sess = requests.Session()
        self.sess.headers.update({'User-Agent':self.ua})
    
    def js(self, link):
        if 'p3p' in link:
            print 'p3p'
            src = 'http://www.p3g.tv/membedplayer/{channel}/{g}/{width}/{height}'
        elif 'vlive' in link:
            print 'vlive'
            src = 'http://www.vlive.pw/embed.php?player=desktop&tk=2598399&live={fid}&vw={vw}&vh={vh}'
        elif 'nowlive' in link:
            print 'nowlive'
            src = 'http://nowlive.pro/stream/{c}/{id}.html'
        elif 'ezcast' in link:
            print 'ezcast'
            src = 'http://www.embedezcast.com/membed/{channel}/{g}/{width}/{height}'
        elif 'ucasterplayer' in link:
            print 'ucasterplayer'
            src = 'http://www.ucasterplayer.com/embedplayer/{channel}/{g}/{width}/{height}'
        elif 'crichd' in link:
            print 'crichd'
            src = 'http://cdn.crichd.im/embed2.php?id={id}&vw={vw}&vh={vh}'
        elif 'capodeportes' in link:
            print 'capodeportes'
            src = 'http://capodeportes.net/reproductor2/{fid}.php?width={width}&height={height}'
        elif 'jazztv' in link:
            print 'jazztv'
            src = 'http://www.jazztv.co/embedx.php?live={fid}&vw={vw}&vh={vh}'
        elif 'playerfs' in link:
            print 'playerfs'
            src = 'http://www.playerfs.com/membedplayer/{channel}/{g}/{width}/{height}'