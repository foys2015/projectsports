import requests
import json
import re

def scrape(sport=None, league=None, team=None):
    if sport is None and team is None:
        return []
    #league is useless for this hive
    base = 'https://streamingsports.me'
    session = requests.Session()
    tables = re.compile('<table.+?>(.+?)</table>', re.DOTALL)
    link = re.compile('<tr>.+?<td>.+?</td>\s+<td>.*?</td>\s+<td>.+?</td>\s+<td.+?>\s+<\!\-\-\s+<a\shref=["\'](.+?)["\']', re.DOTALL)
    
    if team is None:
        if sport.lower() == 'soccer':
            search = ''.join([base, '/football'])
        elif sport.lower() == 'football':
            search = ''.join([base, '/american-football'])
        elif sport.lower() == 'basketball':
            search = ''.join([base, '/basketball'])
        elif sport.lower() == 'hockey':
            search = ''.join([base, '/ice-hockey'])
        elif sport.lower() == 'baseball':
            search = ''.join([base, '/baseball'])
        elif sport.lower() == 'tennis':
            search = ''.join([base, '/tennis'])
        elif sport.lower() == 'motorsports':
            search = ''.join([base, '/motorsports'])
        elif sport.lower() == 'racing':
            search = ''.join([base, '/motorsports'])
        else:
            return []
        sport_page = session.get(search).content
        targetsRE = re.compile('class="event-tr-row\s*clickable-row\s*"\s*data-href="(.+?)"')
        targets = targetsRE.findall(sport_page)
        links = []
        for target in targets:
            tUrl = ''.join([base, target])
            eventPage = session.get(target).content
            #We want the HTTP/Web table, which is last
            linkTable = tables.findall(eventPage)[-1]
            links.extend(link.findall(linkTable))
    else:
        session.headers.update({'Content-Type': 'application/json', 'Referer': base})
        team = team.lower()
        search = ''.join([base, '/search/', team.replace(' ','%20')])
        search_results = json.loads(session.get(search).text)
        if len(search_results) > 0:
            for result in search_results:
                if any([team in result['home_name'].lower(), team in result['away_name'].lower()]):
                    target = ''.join([base, result['detail_match_url']])
                    eventPage = session.get(target).content
                    #We want the HTTP/Web table, which is last
                    linkTable = tables.findall(eventPage)[-1]
                    links = link.findall(linkTable)
                    break
                else:
                    links = []
            return links
        else:
            return []