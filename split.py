import os
import pandoc
from pandoc.types import Pandoc, Header

def split(filepath):
    with open(filepath) as f:
        tree = pandoc.read(f.read())
    [meta, blocks] = tree
    dict = {}

    for i in range(len(blocks)):
        if isinstance(blocks[i], Header):
            level = blocks[i][0]
            if level == 1:
                content = []
                h1Label = blocks[i][1][0]
                fatherLabel = None
                currentLabel = h1Label
                content.append(blocks[i])
            if level == 2:
                content = []
                h2Label = blocks[i][1][0]
                fatherLabel = h1Label
                currentLabel = h2Label
                content.append(blocks[i])

        if not(isinstance(blocks[i], Header)):
            # print(type(blocks[i]))
            content.append(blocks[i])

        # print('processed '+currentLabel)

        dictitem = {currentLabel : (
                level,
                fatherLabel,
                Pandoc(meta, content)
            )
        }

        dict.update(dictitem)

    # print(dict)

    return(dict)




if __name__=="__main__":
    filepath = 'C:/Users/sylva/Documents/latex shit/htmlcss/minimal.md'
    splitteddict = split(filepath)
    dirname = filepath.split('.')[0]+'/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for key in splitteddict:
        item = splitteddict[key]
        if item[1] == None:
            path = key
        else:
            path = item[1]+'/'+key
            if not os.path.exists(dirname+item[1]):
                os.mkdir(dirname+item[1])
        filename = dirname + path + '.md'
        output = pandoc.write(item[2],file=filename , format='markdown')
