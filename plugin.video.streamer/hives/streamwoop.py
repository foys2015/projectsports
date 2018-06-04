import requests
import base64
import json
import re

legend = {'Baseball':'baseball','Basketball':'basketball','Soccer':'soccer-1',
          'Football':'football','Fighting':'boxing','Ice Hockey':'icehockey',
          'Tennis':'tennis-1','Handball':'handball','Volleyball':'volleyball',
          'Rugby':'rugby','Racing':'racing','Golf':'golf'}
          
def scrape(sport, team=None):
    sport = team
    base = 'https://streamwoop.net'
    gamesLink = base + '/sport/{sport}'.format(sport=legend[sport])
    gameLinks = re.compile('<a style="text-decoration: none" href=(.+?)>')
    linksPage = re.compile('Links have moved to a new page. <strong><a href="(.+?)">')
    basedSources = re.compile('https://streamwoop.net/go/(.+?)[">]')
    session = requests.Session()
    gamesPage = session.get(gamesLink).content
    games = gameLinks.findall(gamesPage)
    streams = []
    for game in games:
        resp = session.get(base+game).content
        linksLink = linksPage.findall(resp)[0]
        linkListings = session.get(base+linksLink).content
        basedLinks = basedSources.findall(linkListings)
        for link in basedLinks:
            streams.append(base64.b64decode(link))
    return streams