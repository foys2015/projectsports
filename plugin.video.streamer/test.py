import tb

links = tb.searchHivesFor('mlb')
if len(links) > 0:
    results = tb.tryResolving(links)
    print results
else:
    print 'No results found'
