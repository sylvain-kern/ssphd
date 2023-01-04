'''working!!!
'''

from pandocfilters import toJSONFilters, Link

extension = '.html'
LinkDict = {}

def generate_new_links(key, value, format, meta):
    '''passes through the doc and fills LinkDict = {link of header hn | link of h1 or h2 that contains hn}
        needs to take references from image, table, eq links
    '''

    global LinkDict
    global currentFileLabel

    if key == 'Header':
        [level, [label, t1, t2], header] = value
        if level <= 2:
            currentFileLabel = label
            LinkDict[label] = label
        else:
            LinkDict[label] = currentFileLabel


def set_links(key, value, format, meta):
    '''for all links, detects if it points to an header (contained in LinkDict), and replaces with the good link
    ok
    '''

    global LinkDict
    global currentFileLabel

    if key == 'Header':
        [level, [label, t1, t2], header] = value
        if level <= 2:
            currentFileLabel = label

    if key == 'Link':
        [t1, linktext, [href, t4]] = value
        if href[1:] in LinkDict:
            if LinkDict[href[1:]] != currentFileLabel:
                newhref = LinkDict[href[1:]]+'.html'+href
                return Link(t1, linktext, [newhref, t4])



if __name__=='__main__':
    toJSONFilters([generate_new_links, set_links])