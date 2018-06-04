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
searchTerm = dialog.input('Enter team', type=xbmcgui.INPUT_ALPHANUM)
if searchTerm != '':
    import tb
    links = tb.searchHivesFor(sport=None, team=searchTerm)
    if len(links) > 0:
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