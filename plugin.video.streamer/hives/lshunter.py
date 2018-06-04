import requests
import json
import re

def scrape(sport, team=None):
    base = 'http://www.lshunter.net'
    session = requests.Session()
    livePage = session.get(base+'/ls/section.php?sid=1&bet365=&unibet=').content
    
    
    games = re.compile('<!-- main container of a slide -->(.+?)<!-- close main container of a slide -->', re.DOTALL)
    
    starttime = re.compile('class="lshstart_time">(.+?)<')
    teams = re.compile('class="lshevent">(.+?)<')
    sport = re.compile('class="section">(.+?)<')
    league = re.compile('class="category">(.+?)<')
    date = re.compile('class="date">(.+?)<')
    streams = re.compile('<a href="javascript: void\(0\)" onclick="window.open\(\'(.+?)\'\)')
    
    links = []
    for game in games.findall(livePage):
        links.extend(streams.findall(game))
    return links