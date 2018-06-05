import requests
import json
import re

legend = {'soccer':'football','football':'am-football','hockey':'hockey',
          'nba':'basketball','mlb':'baseball','Baseball':'baseball',
          'golf':'golf','rugby':'rugby','atp':'tennis','wtp':'tennis',
          'pga':'golf','wpga':'golf'}
          
def scrape(sport=None, league=None, team=None):
    #league is useless for this hive
    base = 'http://www.usagoals.nu'
    games = base + '/webmaster/{sport}.html'.format(sport=legend[sport.lower()])
    session = requests.Session()

    link1 = re.compile('<div\s*class=["\']link["\']><a.+?title=["\'](.+?)["\'].+?href=["\'](.+?)["\']', re.DOTALL)
    game_results = session.get(games).content
    firstSet = link1.findall(game_results)
    if len(firstSet) > 0:
        links = []
        for link in firstSet:
            if not team.lower() in link[0]:
                continue
            if link[1].startswith('/'):
                link[1] = ''.join([base, link[1]])
            #print link
            link_page = session.get(link[1]).content
            try:
                #Some pages have iframes
                actualLink = re.compile('<iframe.+?src=["\'](.+?)["\']').findall(link_page)[0]
            except:
                #Most have divs with links in data or src tag
                actualLink = re.compile('<div\s*id=["\']embed-video["\'].+?(?:data|src)=["\'](.+?)["\']', re.DOTALL).findall(link_page)[0]
                #We can adjust this later, but for now I don't know how to structure swfs for playing in kodi
                if '.swf' in actualLink:
                    continue
            #if tinypic or betting keywords are in the link that indicates that the game isn't live yet
            if not 'tinypic' in actualLink and not 'betting' in actualLink:
                links.append(actualLink)
        return links
    else:
        return []