import requests
import json
import re

def scrape(sport=None, league=None, team=None):
    base = 'http://www.lshunter.net'
    session = requests.Session()
    livePage = session.get(base+'/ls/section.php?sid=1&bet365=&unibet=').content
    
    
    games = re.compile('<!-- main container of a slide -->(.+?)<!-- close main container of a slide -->', re.DOTALL)
    
    starttimeRE = re.compile('class="lshstart_time">(.+?)<')
    teamsRE = re.compile('class="lshevent">(.+?)<')
    sportRE = re.compile('class="section">(.+?)<')
    leagueRE = re.compile('class="category">(.+?)<')
    dateRE = re.compile('class="date">(.+?)<')
    streamsRE = re.compile('<a href="javascript: void\(0\)" onclick="window.open\(\'(.+?)\'\)')
    
    links = []
    for game in games.findall(livePage):
        keep = False
        if sport is not None and sport in sportRE.findall(game)[0]:
            keep = True
        if league is not None and league in leagueRE.findall(game)[0]:
            keep = True
        if team is not None and team in teamRE.findall(game)[0]:
            keep = True
        if keep is True:
            links.extend(streamsRE.findall(game))
    return links