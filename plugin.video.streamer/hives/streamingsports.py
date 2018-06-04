import requests
import json
import re

def scrape(sport, team=None):
    if team is None:
        return []
    base = 'https://streamingsports.me'
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json', 'Referer': base})
    team = team.lower()
    search = ''.join([base, '/search/', team.replace(' ','%20')])
    tables = re.compile('<table.+?>(.+?)</table>', re.DOTALL)
    link = re.compile('<tr>.+?<td>.+?</td>\s+<td>.*?</td>\s+<td>.+?</td>\s+<td.+?>\s+<\!\-\-\s+<a\shref=["\'](.+?)["\']', 
                       re.DOTALL)
    search_results = json.loads(session.get(search).text)
    if len(search_results) > 0:
        for result in search_results:
            if any([team in result['home_name'].lower(), team in result['away_name'].lower()]):
                target = ''.join([base, result['detail_match_url']])
                eventPage = session.get(target).content
                #We want the HTTP/Web table, which is last
                linkTable = tables.findall(eventPage)[-1]
                links = link.findall(linkTable)
                print 'here are the links'
                print links
                break
            else:
                links = []
        return links
    else:
        return []