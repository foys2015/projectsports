import importlib
import sources
import hives
import re

sequence = re.compile('^(?:https://|http://|)(?:www\.|)(?:(?=\w+\W)\w+\W|)(\w+[^\W])\.')


def searchHivesFor(sport=None, league=None, team=None):
    results = []
    for hive in hives.__all__:
        theHive = importlib.import_module('hives.' + hive)
        results.extend(theHive.scrape(sport, league, team))
    #Returns links of stream hosts
    return results

#Try to resolve each link
def tryResolving(links):
    streams = []
    for link in links:
        if isResolvable(link):
            while(isResolvable(link)):
                link = resolve(link)
                if isValid(link):
                    streams.append(link)
                    break
            if not link in streams:
                print 'No module found for (%s)' % getBase(link)
        else:
            print 'No module found for (%s)' % getBase(link)
            print link
    #Returns streams of stream hosts
    return streams
    
def resolve(url):
    src = importlib.import_module('sources.' + getBase(url))
    return src.resolve(url)
    
#Helper function to check for existing source module
def isResolvable(url):
    if getBase(url) in sources.__all__:
        return True
    else:
        return False
        
#Helper function check if link is valid streaming link
def isValid(url):
    if any(['.m3u8' in url,'.ts' in url,'rtmp:' in url]):
        return True
    else:
        return False

#Helper function to get module-friendly source name
def getBase(url):
    return sequence.findall(url.replace('-',''))[0]