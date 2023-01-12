import shutil
import os
import pandoc
from pandoc.types import Pandoc, Header, MetaType, MetaInlines, Str

def get_destination(source):
    return source.split('.')[0]+'/'

def generate_nav(source):
    destination = get_destination(source)
    if not os.path.exists(destination):
        os.mkdir(destination)
    # print('pandoc "' + source + '" -o "'+ destination +'nav.md" --number-sections --template="toc-template.md" --toc')
    os.system('pandoc "' + source + '" -o "'+ destination +'nav.md" --number-sections --template="'+destination+'toc-template.md" --toc')
    os.system('pandoc "' + destination + 'nav.md" -o "' + destination + 'nav.html" --filter links-filter-toc.py')


def get_nav(source):
    destination = get_destination(source)
    with open(destination+'nav.html', 'r') as n:
        nav = n.read()
    return nav

def get_split_dict(source):
    with open(source, 'r', encoding='utf8') as f:
        tree = pandoc.read(f.read(), format='json')
    [meta, blocks] = tree
    dict = {}
    offset = [-1, -1]
    for i in range(len(blocks)):
        if isinstance(blocks[i], Header):
            level = blocks[i][0]
            if level == 1:
                content = []
                h1Label = blocks[i][1][0]
                fatherLabel = None
                currentLabel = h1Label
                content.append(blocks[i])
                offset[0] += 1
                offset[1] = -1
            if level == 2:
                content = []
                h2Label = blocks[i][1][0]
                fatherLabel = h1Label
                currentLabel = h2Label
                content.append(blocks[i])
                offset[1] += 1

        if not(isinstance(blocks[i], Header)):
            # print(type(blocks[i]))
            content.append(blocks[i])
        elif not blocks[i][0] <= 2:
            content.append(blocks[i])


        currentMeta = [{}]
        currentMeta[0].update(meta[0])
        currentMeta[0].update({
            'offset': MetaInlines([Str(str(offset[0]) + ',' + str(offset[1]))])

        })

        dictitem = {currentLabel : {
                'level': level,
                'fatherlabel': fatherLabel,
                'offset': str(offset[0]) + ',' + str(offset[1]),
                'pandoc': Pandoc(currentMeta, content)
            }
        }

        dict.update(dictitem)

    return(dict)

def split_json(source):
    splitteddict = get_split_dict(source)
    dirname = get_destination(source)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for key in splitteddict:
        item = splitteddict[key]
        if item['fatherlabel'] == None:
            path = key
        else:
            path = item['fatherlabel']+'/'+key
            if not os.path.exists(dirname+item['fatherlabel']):
                os.mkdir(dirname+item['fatherlabel'])
        filename = dirname + path + '.json'
        output = pandoc.write(item['pandoc'],file=filename , format='json')

def split_md(source):
    splitteddict = get_split_dict(source)
    dirname = get_destination(source)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for key in splitteddict:
        item = splitteddict[key]
        if item['fatherlabel'] == None:
            path = key
        else:
            path = item[1]+'/'+key
            if not os.path.exists(dirname+item['fatherlabel']):
                os.mkdir(dirname+item['fatherlabel'])
        filename = dirname + path + '.md'
        output = pandoc.write(item['pandoc'],file=filename , format='markdown')

def build_html(source):
    dirname = get_destination(source)
    for (root, dirs, files) in os.walk(dirname):
        if not root.endswith('/'):
            root = root+'/'
        for file in files:
            if file.endswith('.json') and not file=='refs.json':
                with open(root + file, 'r', encoding='utf8') as f:
                    meta = pandoc.read(f.read(), format='json')[0][0]
                offset = meta['offset'][0][0][0]
                print(offset)
                command = 'pandoc "' + root + file + '" -s -o "'+ root + file.split('.')[0] +'.html" --title="Titre!" --template="'+dirname+'template-section.html" --number-sections --number-offset=' + offset + ' --css="style.css" --katex --bibliography="refs.json" --csl="nature.csl" --citeproc --metadata-file="'+dirname+'meta.yaml" --filter pandoc-sidenote -V base="file:///'+dirname+'"'
                print(command)
                print()
                os.system(command)
                print()
                print()

def pre_filters(source):
    destname = source.split('.')[0]+'_prefiltered.json'
    print(destname)
    command = 'pandoc "' + source + '" -o "' + destname + '" --filter savelinkdict.py --filter pandoc-xnos --filter links-filter.py --number-sections --filter pandoc-secnos'
    os.system(command)
    print(command)
    return destname

def main(source):
    prefiltered = pre_filters(source)
    generate_nav(prefiltered)
    split_json(prefiltered)
    build_html(prefiltered)


if __name__=='__main__':
    main(source = 'C:/Users/sylva/Documents/latex shit/htmlcss/minimal.md')