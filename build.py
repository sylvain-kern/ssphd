import shutil
import os
import pandoc
import argparse
import re
import json

import matplotlib.pyplot as plt, mpld3
import pickle as pkl
import pandocfilters as pf

# from inspect import getsourcefile
# from pandoc.types import Pandoc, Header, MetaType, MetaInlines, MetaBool, Str
from mpld3 import plugins


ABOUT = "The ultimate document processor."


class Document:

    def __init__(self, source):

        self.source_file    = source
        self.root_path      = os.path.dirname(os.path.abspath(self.source_file))
        self.dest_path      = self.source_file.split('.')[0]+'/'
        self.config_file    = os.path.join(self.root_path, 'config.yaml')
        self.meta_file      = os.path.join(self.root_path, '_assets/meta/meta.yaml')
        self.assets_path    = os.path.join(self.root_path, '_assets')
        self.templates_path = os.path.join(self.dest_path, '_assets/templates')
        self.css_path       = os.path.join(self.root_path, '_assets/css')
        self.pictures_path  = os.path.join(self.root_path, '_assets/pics')
        self.refs_path      = os.path.join(self.root_path, '_assets/refs')

        with open(self.source_file, 'r', encoding='utf8') as f:
            content = f.read()
        self.ast = pandoc.read(
            content,
            options=[
            ])

        self.abbreviation_definitions = {}
        self.link_dict = {}
        self.path = ['', '']
        self.structure_list = []

    ## FILTERS

    def add_title_to_references(self, key, value, format_, meta):
        if key == "Div" and "refs" in value[0][0]:
            attrs, children = value
            t1 = ["unnumbered"]
            t2 = []
            title = pf.Header(1, ["references", t1, t2], [pf.Str("References")])
            return [title, pf.Div(attrs, children)]

    def get_abbreviation_definitions(self, key, value, format_, meta):
        abbr_def_pattern = r'\+\[(.*?)\]:\s(.*?)$'
        if key == 'Para':
            text = pf.stringify(value)
            match = re.match(abbr_def_pattern, text)
            if match:
                abbreviation, description = match.groups()
                self.abbreviation_definitions[abbreviation] = description
                return []

    def replace_abbreviations(self, key, value, format_, meta):
        if key == 'Str':
            text = value
            abbr_start = text.find('+[')
            if abbr_start >= 0:
                abbr_end = text.find(']', abbr_start)
                if abbr_end > abbr_start + 2:
                    # Search for the end of the abbreviation, including any non-space characters
                    abbr_text = text[abbr_start + 2:abbr_end]
                    following_char = text[-1]
                    if following_char=="]":
                        following_char = ""

                    abbr_definition_start = abbr_end + 1
                    abbr_definition = text[abbr_definition_start:]
                    if abbr_text in self.abbreviation_definitions:
                        abbr_description = self.abbreviation_definitions[abbr_text]
                        abbr_html = f'<abbr title="{abbr_description}">{abbr_text}</abbr>{following_char}'
                        return pf.RawInline('html', abbr_html)

    def generate_link_dict(self, key, value, format_, meta):

        if key == 'Header':
            [level, [label, t1, t2], header] = value
            if level == 1:
                self.path[0] = label
                self.filelabel = label
                self.link_dict[label] = self.filelabel
            elif level == 2:
                self.path[1] = label
                self.filelabel = self.path[0] + '/' + self.path[1]
                self.link_dict[label] = self.filelabel
            elif level > 2:
                self.filelabel = self.path[0] + '/' + self.path[1]
                self.link_dict[label] = self.filelabel + '/#' + label


        # if key == 'Para' and len(value) == 1 and \
        #     value[0]['t'] == 'Image' and value[0]['c'][-1][1].startswith('fig:'):
        #     label = value[0]['c'][0][0]
        #     LinkDict[label] = currentFileLabel

        if key in ('Div', 'Image', 'Equation'):
            # print(value)
            label = value[0][0]
            # print(label)
            # print(filelabel)
            self.link_dict[label] = self.filelabel + '/#' + label

        # with open('links.json', 'w') as f:
        #     json.dump(self.link_dict, f)


    def links_filter(self, key, value, format_, meta):
        if key == 'Link':
            [t1, linktext, [href, t4]] = value
            ref = href[1:]
            if ref in self.link_dict:
                newhref = self.link_dict[ref]
                return pf.Link(t1, linktext, [newhref, t4])

    ## OPERATIONS

    def copy(self, ast, opts):
        return pandoc.read(pandoc.write(ast), options=opts)

    def pipe(self, opts):
        self.ast = pandoc.read(pandoc.write(self.ast), options=opts)

    def filter(self, handles, ast=None):
        if ast==None:
            doc = pf.json.loads(pandoc.write(self.ast, format='json'))
            for handle in handles:
                doc = pf.walk(doc, handle, "", None)
            self.ast = pandoc.read(pf.json.dumps(doc), format='json')
        else:
            doc = pf.json.loads(pandoc.write(ast, format='json'))
            for handle in handles:
                doc = pf.walk(doc, handle, "", None)
            return pandoc.read(pf.json.dumps(doc), format='json')

    def build_folder_structure(self):
        if not os.path.exists(self.dest_path + '_assets/'):
            shutil.copytree(self.assets_path, self.dest_path + '_assets/')

    # FLOATS

    def get_d3(self, pkl_fig_path):
        with open(pkl_fig_path, 'rb') as f:
            fig = pkl.load(f)
        ax = fig.gca()
        css = """
        table
        {
        border-collapse: collapse;
        }
        th
        {
        color: #ffffff;
        background-color: #000000;
        }
        td
        {
        background-color: #cccccc;
        }
        table, th, td
        {
        font-family:Arial, Helvetica, sans-serif;
        border: 1px solid black;
        text-align: right;
        }
        """
        for line in ax.get_lines():
                # get the x and y coords
                xy_data = line.get_xydata()
                labels = []
                for x, y in xy_data:
                        # Create a label for each point with the x and y coords
                        html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                        labels.append(html_label)
        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
        plugins.connect(fig, tooltip)
        html = mpld3.fig_to_html(fig)
        with open("_assets/graphs/test.html", "w") as f:
            f.write(html)
        return html

    # STRUCTURE

    def generate_nav(self):
        self.nav = pandoc.write(
            self.ast,
            format="html",
            # file= self.templates_path+"/nav.html",
            options=[
                "--number-sections",
                "--template="+self.templates_path+"/template-toc.html",
                "--toc",
                "--toc-depth=2",
            ])
        self.nav = pandoc.read(self.nav, format="html")
        self.extract_structure()
        self.nav = self.filter([self.links_filter], ast=self.nav)
        pandoc.write(
            self.nav,
            file = self.templates_path+"/nav.html",
            format = "html"
        )

    def extract_structure(self):
        markdown_list = pandoc.write(self.nav, format="markdown", options=["--wrap=none", "--toc-depth=6"])

        structure_dict = {}
        lines = markdown_list.split("\n")

        # regexes to match the bullet list lines
        pattern_numbered = r"\[\[(.*?)\]\{\.toc-section-number\} (.*?)\]\(#(.*?)\)\{#.*?\}"
        pattern_numbered_bis = r"\[(.*?)\] (.*?)"
        pattern_unnumbered = r"\[(.*?)\]\(#(.*?)\)\{#.*?\}"
        level = 1
        parents = [None]

        for line in lines[:-1]:
            [indents, str] = line.split("-   ")
            # print(line)
            nindents = len(indents)//4+1
            diff = nindents - level
            if diff > 0:
                parents.append(id)
            elif diff < 0:
                parents = parents[:diff]

            level+=diff
            # getting the id and number by matching
            match_numbered = re.search(pattern_numbered, str)
            match_numbered_bis = re.search(pattern_numbered_bis, str)
            match_unnumbered = re.search(pattern_unnumbered, str)
            # print(match_numbered)
            # print(match_numbered_bis)
            # print(match_unnumbered)

            if match_numbered:
                number = match_numbered.group(1)
                title = match_numbered.group(2)
                id = match_numbered.group(3)
            elif match_numbered_bis:
                number = match_numbered_bis.group(1)
                title = match_numbered_bis.group(2)
                id = None
            elif match_unnumbered:
                title = match_unnumbered.group(1)
                id = match_unnumbered.group(2)
                number=None

            structure_dict[id] = {
                "title": title,
                "level": level,
                "number": number,
                "parent": parents[-1],
                "children": []
            }

            if level <= 2:
                self.structure_list.append(id)

        for key, val in structure_dict.items():
            if val["parent"] != None:
                structure_dict[val["parent"]]["children"].append(key)

        # print(structure_dict)
        # with open('structure.json', 'w') as f:
        #     json.dump(structure_dict, f)

        self.structure_dict = structure_dict

    def split_structure(self):
        for key, val in self.structure_dict.items():
            id = key
            level = val["level"]
            if level == 1:
                if not os.path.exists(self.dest_path + key):
                    os.mkdir(self.dest_path + key)
                for child in val["children"]:
                    if not os.path.exists(self.dest_path + key + '/' + child):
                        os.mkdir(self.dest_path + key + '/' + child)

    # GRAPHS

    def graphs_filter(self, key, value, format, meta):
        # if key == 'Image':
        #     [_, _, attrs] = value
        #     alt_text = pf.stringify(value[1])
        #     src = attrs[0][1]
        #     custom_html = f'<div class="custom-img"><img src="{src}" alt="{alt_text}"></div>'
        #     return [{"custom_html": custom_html}, []]  # Include as metadata
        pass

    def get_next(self, key):
        index = self.structure_list.index(key)
        if index == len(self.structure_list):
            return "", ""
        else:
            nextkey = self.structure_list[index + 1]
        number = self.structure_dict[nextkey]["number"]
        if number == None:
            prefix = ""
        else:
            prefix = number + " "
        return self.link_dict[nextkey],  prefix + self.structure_dict[nextkey]["title"]

    def get_prev(self, key):
        index = self.structure_list.index(key)
        if index == 0:
            return "", ""
        else:
            prevkey = self.structure_list[index - 1]
        number = self.structure_dict[prevkey]["number"]
        if number == None:
            prefix = ""
        else:
            prefix = number + " "
        return self.link_dict[prevkey], prefix + self.structure_dict[prevkey]["title"]

    # S P L I T

    def split(self):
        [meta, blocks] = self.ast
        # os.mkdir('./trash/')
        content = []
        reset = 0
        for block in blocks:
            if isinstance(block, pandoc.types.Header):
                level = block[0]
                if level <= 2:
                    if content != []:
                        slice = pandoc.types.Pandoc(meta, content)
                        offset = self.structure_dict[key]["number"] or "0"
                        if offset != "0": # V   1 -> 0, 1.1 -> 1.0, 1.1.1 -> 1.1.0
                            offset = ".".join(item for item in [".".join(offset.split(".")[:-1]) , str(int(offset.split(".")[-1])-1)] if item and item != "")
                        next, nexttitle = self.get_next(key)
                        prev, prevtitle = self.get_prev(key)
                        pagetitle = self.structure_dict[key]["title"]
                        if next != "":
                            hasnext = "true"
                        else:
                            hasnext = ""
                        if prev != "":
                            hasprev = "true"
                        else:
                            hasprev = ""
                        content = []
                        if mylevel == 1:
                            file = self.dest_path + key + '/index.html'
                            ischapter = "true"
                            parent = ""
                            parenttitle = ""
                        elif mylevel == 2:
                            file = self.dest_path + self.structure_dict[key]["parent"]  + '/' + key + '/index.html'
                            ischapter = ""
                            parent = self.structure_dict[key]["parent"]
                            parenttitle = self.structure_dict[parent]["number"] + " " + self.structure_dict[parent]["title"]
                        pandoc.write(slice,
                            file = file,
                            format = "html",
                            options = [
                                "--standalone",
                                "--katex",
                                "--filter=pandoc-plot",
                                "--template="+self.dest_path+"_assets/templates/template-section.html",
                                "--variable=base=/",
                                "--variable=pagetitle="+pagetitle,
                                "--variable=ischapter:"+ischapter,
                                "--variable=parent="+parent,
                                "--variable=parenttitle="+parenttitle,
                                "--variable=hasprev="+hasprev,
                                "--variable=prev="+prev,
                                "--variable=prevtitle="+prevtitle,
                                "--variable=hasnext="+hasnext,
                                "--variable=next="+next,
                                "--variable=nexttitle="+nexttitle,
                                "--number-sections",
                                "--number-offset="+offset.replace(".", ","),
                                "--toc-depth=3",
                                "--section-divs",
                                "--filter=pandoc-sidenote"
                            ])
                    key = block[1][0]
                    mylevel = level
            content.append(block)

    def put_to_htdocs(self):
        if os.path.exists('C://Apache24/htdocs/'):
            shutil.rmtree('C://Apache24/htdocs/')
        shutil.copytree(self.dest_path, 'C://Apache24/htdocs/')

    def generate_index(self):
        pandoc.write(
            self.ast,
            file = self.dest_path + '/index.html',
            options = [
                "--template="+self.dest_path+"_assets/templates/template-index.html"
            ]
        )

    def generate_404():
        pass


def main():

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="Path to a Markdown source file.")

    args = parser.parse_args()

    args.markdown_source = os.path.abspath(args.markdown_source)

    # print(args.markdown_source)

    doc = Document(args.markdown_source)
    doc.build_folder_structure()

    meta = doc.ast[0] # saving metadata bc it seems overriden by --metadata-file

    doc.pipe(
        [
            "--metadata-file=_assets/meta/meta.yaml",
            # "--csl=_assets/refs/nature.csl",
            # "--filter=_assets/filters/title_above_references.py",
            # "--number-sections",
            # "--katex",
            # "--filter=pandoc-xnos",
            # "--filter=pandoc-secnos",
            "--filter=pandoc-crossref",
            "--bibliography=_assets/refs/refs.json",
            "--citeproc",
        ]
    )

    doc.ast[0] = pandoc.types.Meta(doc.ast[0][0] | meta[0]) # merge yaml block with metadata from metadata file

    doc.filter([
        doc.add_title_to_references,
        doc.get_abbreviation_definitions,
        doc.replace_abbreviations,
        doc.generate_link_dict,
        doc.links_filter
    ])

    doc.generate_nav()
    doc.filter([doc.graphs_filter])
    doc.split_structure()

    doc.split()

    doc.generate_index()


    # pandoc.write(
    #     doc.ast,
    #     file="simpletext.html",
    #     format="html",
    #     options=[
    #         "--standalone",
    #         "--number-sections",
    #         # "--filter=pandoc-eqnos",
    #         "--katex",
    #         "--filter=pandoc-plot",
    #         "--template=_assets/templates/template-section.html",
    #         "--css=_assets/css/style.css",
    #         "--section-divs",
    #         "--variable=base=C:/Users/sylva/Documents/latex shit/htmlcss"
    #     ])


    doc.put_to_htdocs()


if __name__=='__main__':
    main()