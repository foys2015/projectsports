import xbmcplugin
import xbmcaddon
import xbmcgui
import sys

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_id = 'plugin.video.streamer'
addon = xbmcaddon.Addon(id=addon_id)
addonname = addon.getAddonInfo('name')
path = 'special://home/addons/%s/' % addon_id
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
dialog = xbmcgui.Dialog()

#This is only for the testing phases
#Obviously we will adjust this to programatically 
#provide the values instead of showing a dialog when moving to production
#Value must ALWAYS include 2 pipes (|)
#Acceptable examples value formats are:
#Baseball|None|None
#Baseball|MLB|None
#Baseball|MLB|Philadelphia Phillies
#None|MLB|None
#None|MLB|Philadelphia Phillies
#None|None|Philadelphia Phillies
searchVars = dialog.input('Enter sport|league|team (in that format)', type=xbmcgui.INPUT_ALPHANUM)
if searchVars != '':
    import tb
    vals = searchVars.split('|')
    #Using eval() in order to convert None strings to python's None
    links = tb.searchHivesFor(sport=eval(vals[0]), league=eval(vals[1]), team=eval(vals[2]))
    if len(links) > 0:
        #Commented out for now to make sure we're grabbing initial links from hives
        #results = tb.tryResolving(links)
        #for link in results:
        for link in links:
            source = tb.getBase(link)
            list_item = xbmcgui.ListItem(path=link, label=source)
            list_item.setInfo('video', {'title': source})
            list_item.setProperty('IsPlayable','true')
            xbmcplugin.addDirectoryItem(_handle, link, list_item, False)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(_handle)
    else:
        line1 = 'Sorry, no live links were found for the match.'
        dialog.ok(addonname, line1)