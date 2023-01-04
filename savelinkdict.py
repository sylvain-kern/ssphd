from pandocfilters import toJSONFilter
import json

LinkDict = {}

def generate_link_dict(key, value, format, meta):
    '''passes through the doc and fills LinkDict = {link of header hn | link of h1/h2 that contains hn}
        needs to take references from image, table, eq links
    '''

    global LinkDict
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

    if key in ('Table', 'Image'):
        label = value[0][0]
        LinkDict[label] = currentFileLabel

    if key == 'Para' and value[0]['t'] == 'Math' and value[0]['c'][0]['t'] == 'DisplayMath' and value[-1]['c'][0:4] == '{#eq':
        label = value[2]['c'][2:-1]   # le dièse en moins
        LinkDict[label] = currentFileLabel

    with open('linkdict.json', 'w') as convert_file:
        convert_file.write(json.dumps(LinkDict))

if __name__=='__main__':
    toJSONFilter(generate_link_dict)