import shutil
import os
import pandoc

from inspect import getsourcefile
from pandoc.types import Pandoc, Header, MetaType, MetaInlines, MetaBool, Str


def get_destination(source):
    return source.split('.')[0]+'/'

ROOT_PATH       = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))
SOURCE          = ROOT_PATH +'/test_standalone.md'
CONFIG_FILE     = os.path.join(ROOT_PATH, 'config.yaml')
META_FILE       = os.path.join(ROOT_PATH, 'meta.yaml')
ASSETS_PATH     = os.path.join(ROOT_PATH, '_assets')
TEMPLATES_PATH  = os.path.join(ROOT_PATH, '_assets/templates')
FILTERS_PATH    = os.path.join(ROOT_PATH, '_assets/filters')
CSS_PATH        = os.path.join(ROOT_PATH, '_assets/css')
PICTURES_PATH   = os.path.join(ROOT_PATH, '_assets/pics')
REFS_PATH       = os.path.join(ROOT_PATH, '_assets/refs')
DEST_PATH       = get_destination(SOURCE).split('.')[0]+'/'


def generate_nav(source):
    destination = DEST_PATH
    if not os.path.exists(destination):
        os.mkdir(destination)
    os.system('pandoc "' + source + '" -o "'+ DEST_PATH +'_assets/templates/nav.md" --number-sections --template="'+ DEST_PATH +'_assets/templates/template-toc.md" --toc')
    print('pandoc "' + DEST_PATH + '_assets/templates/nav.md' + '" -o "'+ DEST_PATH + '_assets/templates/nav.html" --template="'+ DEST_PATH +'_assets/templates/template-toc.html" --filter _assets/filters/links-filter-toc.py')
    os.system('pandoc "' + DEST_PATH + '_assets/templates/nav.md' + '" -o "'+ DEST_PATH + '_assets/templates/nav.html" --filter _assets/filters/links-filter-toc.py')


def get_split_dict(source):
    with open(source, 'r', encoding='utf8') as f:
        tree = pandoc.read(f.read(), format='json')
    [meta, blocks] = tree
    dict = {}
    offset = [0, 0]
    for i in range(len(blocks)):
        if isinstance(blocks[i], Header):
            level = blocks[i][0]
            if level == 1:
                if not blocks[i][1][1] == ["unnumbered"]:
                    offset[0] += 1
                offset[1] = 0
                content = []
                currentMeta = [{}]
                currentMeta[0].update(meta[0])
                h1Label = blocks[i][1][0]
                h1Title = pandoc.write(blocks[i], format='plain')
                fatherLabel = None
                fatherTitle = None
                currentLabel = h1Label
                content.append(blocks[i])
                currentMeta[0].update({
                    'ischapter': MetaBool(True)
                })
            if level == 2:
                if not blocks[i][1][1] == ["unnumbered"]:
                    offset[1] += 1
                content = []
                currentMeta = [{}]
                currentMeta[0].update(meta[0])
                h2Label = blocks[i][1][0]
                fatherLabel = h1Label
                fatherTitle = str(offset[0]) + ' ' + h1Title
                currentLabel = h2Label
                content.append(blocks[i])
                currentMeta[0].update({
                    'fatherlabel': MetaInlines([Str(fatherLabel)])
                })
                currentMeta[0].update({
                    'fathertitle': MetaInlines([Str(fatherTitle)])
                })

        if not(isinstance(blocks[i], Header)):
            content.append(blocks[i])
        elif not blocks[i][0] <= 2:
            content.append(blocks[i])

        if offset[1] == 0:
            currentMeta[0].update({
                'offset': MetaInlines([Str(str(offset[0]-1) + ',' + str(offset[1]-1))])

            })
        else:
            currentMeta[0].update({
                'offset': MetaInlines([Str(str(offset[0]) +  ',' + str(offset[1]-1))])

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
    dirname = DEST_PATH
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for key in splitteddict:
        item = splitteddict[key]
        if item['fatherlabel'] == None:
            path = key
            if not os.path.exists(dirname + path):
                os.mkdir(dirname + path)
        else:
            path = item['fatherlabel']+'/'+key
            if not os.path.exists(dirname + path):
                os.mkdir(dirname + path)
        filename = dirname + path + '/index.json'
        output = pandoc.write(item['pandoc'], file=filename, format='json')

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

def build_html():
    dirname = DEST_PATH
    for (root, dirs, files) in os.walk(dirname):
        if not root.endswith('/'):
            root = root+'/'
        for file in files:
            if file.endswith('.json') and not file=='refs.json':
                with open(root + file, 'r', encoding='utf8') as f:
                    meta = pandoc.read(f.read(), format='json')[0][0]
                offset = meta['offset'][0][0][0]
                # print(offset)
                # command = 'pandoc "' + root + file + '" -s -o "'+ root + file.split('.')[0] +'.html" --template="'+dirname+'template-section.html" --number-sections --section-divs --number-offset=' + offset + ' --css="style.css" --katex --citeproc  --filter links-filter.py --filter pandoc-sidenote --filter pandoc-acronyms -V base="file:///'+dirname+'"'
                command = 'pandoc "' + root + file + '" -s -o "'+ root + file.split('.')[0] +'.html" --template="'+DEST_PATH+'/_assets/templates/template-section.html" --number-sections --section-divs --number-offset=' + offset + ' --katex --citeproc  --filter _assets/filters/links-filter.py --filter pandoc-sidenote -V base="/" --csl="_assets/refs/chicago-fullnote-bibliography.csl"'
                # print(command)
                os.system(command)

def pre_filters(source):
    destname = source.split('.')[0]+'.json'
    # print(destname)
    command = 'pandoc "' + source + '" -o "' + destname + '" --filter _assets/filters/savelinkdict.py --filter pandoc-secnos --filter pandoc-crossref --metadata-file="'+DEST_PATH+'/_assets/meta/meta.yaml"'
    os.system(command)
    # print(command)
    return destname

def main(source):
    prefiltered = pre_filters(source)
    generate_nav(prefiltered)
    split_json(prefiltered)
    build_html()

def build_folder_structure():
    if not os.path.exists(DEST_PATH + '_assets/'):
        shutil.copytree(ASSETS_PATH, DEST_PATH + '_assets/')

def generate_index():
    pass

def generate_404():
    pass


if __name__=='__main__':
    build_folder_structure()
    main(source = SOURCE)