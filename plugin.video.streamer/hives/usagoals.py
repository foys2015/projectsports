import requests
import json
import re

legend = {'soccer':'football','football':'am-football','hockey':'hockey',
          'nba':'basketball','mlb':'baseball','golf':'golf','rugby':'rugby',
          'atp':'tennis','wtp':'tennis','pga':'golf','wpga':'golf'}
          
def scrape(sport, team=None):
    sport = team
    base = 'http://www.usagoals.nu'
    games = base + '/webmaster/{sport}.html'.format(sport=legend[sport.lower()])
    print games
    session = requests.Session()

    link1 = re.compile('<div\s*class=["\']link["\']><a.+?href=["\'](.+?)["\']', re.DOTALL)
    game_results = session.get(games).content
    firstSet = link1.findall(game_results)
    #print game_results
    print len(firstSet)
    if len(firstSet) > 0:
        links = []
        for link in firstSet:
            if link.startswith('/'):
                link = ''.join([base, link])
            #print link
            link_page = session.get(link).content
            try:
                actualLink = re.compile('<iframe.+?src=["\'](.+?)["\']').findall(link_page)[0]
            except:
                actualLink = re.compile('<div\s*id=["\']embed-video["\'].+?(?:data|src)=["\'](.+?)["\']', re.DOTALL).findall(link_page)[0]
                if '.swf' in actualLink:
                    continue
            if not 'tinypic' in actualLink and not 'betting' in actualLink:
                links.append(actualLink)
        return links
    else:
        return []