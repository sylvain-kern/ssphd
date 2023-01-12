import pandoc
from pandoc.types import Str, MetaInlines

source = 'C:/Users/sylva/Documents/latex shit/htmlcss/minimal.md'
with open(source, 'r', encoding='utf8') as f:
    tree = pandoc.read(f.read(), format='markdown')
[meta, blocks] = tree
print(meta)
print(meta[0])
meta[0].update({
    'number-offset': MetaInlines([Str('1,2')])
})
print(meta[0]['number-offset'][0][0][0])