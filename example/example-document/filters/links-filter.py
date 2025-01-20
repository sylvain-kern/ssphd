'''working!!!
'''

from pandocfilters import toJSONFilters, Link
import json

def generate_link_dict(key, value, format, meta):
    '''passes through the doc and fills LinkDict = {link of header hn | link of h1 or h2 that contains hn}
        needs to take references from image, table, eq links
    '''

    global LinkDict
    with open('./linkdict.json') as dictfile:
        LinkDict = json.load(dictfile)
    global currentFileLabel
    global currentChapLabel
    global currentSecLabel

    if key == 'Header':
        [level, [label, t1, t2], header] = value
        if level == 1:
            currentChapLabel = label
            currentSecLabel = ''
            currentFileLabel = currentChapLabel
            LinkDict[label] = currentFileLabel
        elif level == 2:
            currentSecLabel = label
            currentFileLabel = currentChapLabel + '/' + currentSecLabel
            LinkDict[label] = currentFileLabel
        else:
            LinkDict[label] = currentFileLabel

    # if key == 'Para' and len(value) == 1 and \
    #     value[0]['t'] == 'Image' and value[0]['c'][-1][1].startswith('fig:'):
    #     label = value[0]['c'][0][0]
    #     LinkDict[label] = currentFileLabel

    if key in ('Table', 'Image'):
        label = value[0][0]
        LinkDict[label] = currentFileLabel

    with open('linkdict.json', 'w') as convert_file:
        convert_file.write(json.dumps(LinkDict))

def set_links(key, value, format, meta):
    '''for all links, detects if it points to an header (contained in LinkDict), and replaces with the good link
    ok
    '''
    global currentFileLabel
    global currentChapLabel
    global currentSecLabel

    with open('./linkdict.json') as dictfile:
        LinkDict = json.load(dictfile)

    if key == 'Header':
        [level, [label, t1, t2], header] = value
        if level == 1:
            currentChapLabel = label
            currentSecLabel = ''
            currentFileLabel = currentChapLabel
        elif level == 2:
            currentSecLabel = label
            currentFileLabel = currentChapLabel + '/' + currentSecLabel
        else:
            currentFileLabel = currentChapLabel + '/' + currentSecLabel

    if key == 'Link':
        [t1, linktext, [href, t4]] = value
        if href[1:] in LinkDict:
            # newhref = LinkDict[href[1:]] + '/index.html/' + href
            newhref = LinkDict[href[1:]] + '/' + href
            return Link(t1, linktext, [newhref, t4])


if __name__=='__main__':
    toJSONFilters([set_links])