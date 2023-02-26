from pandocfilters import toJSONFilters, Link
import json


def set_links(key, value, format, meta):
    '''for all links, detects if it points to an header (contained in LinkDict), and replaces with the good link
    ok
    '''
    with open('./linkdict.json') as dictfile:
        LinkDict = json.load(dictfile)

    if key == 'Link':
        [t1, linktext, [href, t4]] = value
        if href[1:] in LinkDict:
            # newhref = LinkDict[href[1:]] + '/index.html/' + href
            newhref = LinkDict[href[1:]] + '/' + href
            return Link(t1, linktext, [newhref, t4])

if __name__=='__main__':
    toJSONFilters([set_links])