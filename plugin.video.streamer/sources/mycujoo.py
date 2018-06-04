import requests
import json
import re
    
def resolve(link):
    uAgent = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/65.0.3325.181 Safari/537.36')
    session = requests.Session()
    window = re.compile('window\.\_d\s+=\s+(\{.+?\});', re.DOTALL)
    
    stream_page = session.get(link).content
    stream_jsonStr = window.findall(stream_page)[0]
    stream_jsonObj = json.loads(stream_jsonStr)
    
    resolved = '{stream}|Referer={referer}&User-Agent={useragent}'.format(stream=stream_jsonObj['video']['filename'],
                                                                          referer=link, useragent=uAgent)
    return resolved