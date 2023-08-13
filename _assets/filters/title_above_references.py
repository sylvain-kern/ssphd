import pandocfilters as pf

def add_title_to_references(key, value, format, meta):
    if key == "Div" and "refs" in value[0][0]:
        attrs, children = value
        t1 = ["unnumbered"]
        t2 = []
        title = pf.Header(1, ["references", t1, t2], [pf.Str("References")])
        return [title, pf.Div(attrs, children)]

if __name__ == "__main__":
    pf.toJSONFilters([add_title_to_references])