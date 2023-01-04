from pandocfilters import RawBlock, toJSONFilter

def wide(key, value, format, meta):
    if key == "Div":
        [[ident, classes, kvs], contents] = value
        if "wide" in classes:
            if format == "latex":
                return([RawBlock('latex', '\\begin{wide}')] + contents + [RawBlock('latex', '\\end{wide}')])

if __name__=='__main__':
    toJSONFilter(wide)