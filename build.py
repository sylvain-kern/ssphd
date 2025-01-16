import shutil
import os
import pypandoc
import argparse
import re
import json

import pandocfilters as pf

from rich.progress import track

# from inspect import getsourcefile
# from pandoc.types import Pandoc, Header, MetaType, MetaInlines, MetaBool, Str
# from mpld3 import plugins


ABOUT = "The ultimate document processor."


class Document:

    def __init__(self, source):

        self.source_file    = source
        self.root_path      = os.path.dirname(os.path.abspath(self.source_file))
        self.dest_path      = self.source_file.split('.')[0]+'-html/'
        self.latex_path      = self.source_file.split('.')[0]+'-latex/'
        self.config_file    = os.path.join(self.root_path, 'config.yaml')
        self.meta_file      = os.path.join(self.root_path, '_assets/meta/meta.yaml')
        self.assets_path    = os.path.join(self.root_path, '_assets')
        self.templates_path = os.path.join(self.dest_path, '_assets/templates')
        self.css_path       = os.path.join(self.root_path, '_assets/css')
        self.pictures_path  = os.path.join(self.root_path, '_assets/pics')
        self.refs_path      = os.path.join(self.root_path, '_assets/refs')

        self.ast = pypandoc.convert_file(
                self.source_file,
                'json',
                extra_args = [
            ])

        self.graph_count = 0

    ## FILTERS

    def add_title_to_references(self, key, value, format_, meta):
        if key == "Div" and "refs" in value[0][0]:
            attrs, children = value
            t1 = ["unnumbered"]
            t2 = []
            title = pf.Header(1, ["references", t1, t2], [pf.Str("References")])
            return [title, pf.Div(attrs, children)]

    def get_abbreviation_dict(self, key, value, format_, meta):
        abbr_def_pattern = r'\+\[(.*?)\]:\s(.*?)$'
        if key == 'Para':
            text = pf.stringify(value)
            match = re.match(abbr_def_pattern, text)
            if match:
                abbreviation, description = match.groups()
                self.abbreviation_dict[abbreviation] = description
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
                    if abbr_text in self.abbreviation_dict:
                        if abbr_text.isupper():
                            clss = "acronym"
                        else:
                            clss = ""
                        abbr_description = self.abbreviation_dict[abbr_text]
                        abbr_html = f'<abbr title="{abbr_description}" class="{clss}">{abbr_text}</abbr>{following_char}'
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

        if key in ('Div', 'Figure', 'Equation'):
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

    def nav_filter(self, key, value, format_, meta):
        if key == 'BulletList':
            items = []
            for element in value:
                id = element[0]['c'][0]['c'][0][0][4:]
                level = self.structure_dict[id]["level"]
                if level == 2:
                    # print(f"{id} -> {level}")
                    # print(yaml.dump(element))
                    items.append([
                        pf.Div(("", ["toc-dropdown-btn"], []), []),
                    ] + element)
                else:
                    items.append(element)
            return pf.BulletList(items)

    ## OPERATIONS

    def copy(self, ast, opts):
        return pypandoc.convert_text(
            ast,
            to='json',
            format='json',
            extra_args=opts)

    def pipe(self, opts):
        self.ast = self.copy(
            self.ast,
            opts)

    def filter(self, handles, ast=None):
        if ast==None:
            doc = pf.json.loads(self.ast)
            for handle in handles:
                doc = pf.walk(doc, handle, "", None)
            self.ast = pf.json.dumps(doc)
        else:
            doc = pf.json.loads(ast)
            for handle in handles:
                doc = pf.walk(doc, handle, "", None)
            return pf.json.dumps(doc)

    def build_folder_structure(self):
        if not os.path.exists(self.dest_path + '_assets/'):
            shutil.copytree(self.assets_path, self.dest_path + '_assets/')

    # SEARCH

    def generate_search_index(self, key, value, format_, meta):

        self.search_dict = {}

        if key == 'Header':
             [level, [label, t1, t2], header] = value

        elif key == 'Paragraph':
            pass

    # STRUCTURE

    def generate_nav(self):
        print("generating nav")
        self.nav = pypandoc.convert_text(
            self.ast,
            format = "json",
            to="html",
            # file= self.templates_path+"/nav.html",
            extra_args=[
                "--number-sections",
                "--template="+self.templates_path+"/template-toc.html",
                "--toc",
                "--toc-depth=3",
            ])
        self.extract_structure()
        self.nav = pypandoc.convert_text(
            self.nav,
            format = 'html',
            to = 'json'
        )
        self.nav = self.filter([
                self.links_filter,
                self.nav_filter
            ],
            ast=self.nav
        )

        pypandoc.convert_text(
            self.nav,
            format = "json",
            to = "html",
            outputfile = self.templates_path+"/nav.html",
            # extra_args=[
            #     "--number-sections",
            #     "--template="+self.templates_path+"/template-toc.html",
            # ]
        )

    def extract_structure(self):
        markdown_list = pypandoc.convert_text(
            self.nav,
            format="html",
            to="md",
            extra_args=["--wrap=none", "--toc-depth=6"]
        )

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
        print("generating split structure")
        for key, val in track(self.structure_dict.items()):
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
        import csv
        if key == 'Image':
            [ident, stuff, keyvals], caption, [filename, typef] = value
            if filename.split('.')[-1] == 'csv':
                # parsing the data
                with open(filename, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    columns = next(reader)
                xcolumn = columns[0]
                ycolumns = ', '.join(columns[1:])
                kwargs = {}
                kwargs['xlabel'] = xcolumn
                kwargs['ylabel'] = columns[2]
                kwargs['legendPosition'] = 'graph'
                for keyval in keyvals:
                    kwargs[keyval[0]] = keyval[1]
                    print(keyval)
                # formatting the graph
                graph_id = f"dygraph_{self.graph_count}"
                self.graph_count += 1
                graph_script = f"""
                    var {graph_id} = generateGraph(id="{graph_id}", data="{filename}", xdata="{xcolumn}", ydata="{ycolumns}", xlabel="{kwargs['xlabel']}", ylabel="{kwargs['ylabel']}", legendPosition="{kwargs['legendPosition']}");
                """
                graphsjs_file = self.dest_path+'_assets/js/graphs.js'
                with open(graphsjs_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(graph_script)
                return [
                    pf.RawInline("html", f"<div class='graph-container' id={graph_id} legendPosition={kwargs['legendPosition']}></div>")
                ]

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
        print('splitting to html files'),
        # [meta, blocks] = self.ast
        dico = json.loads(self.ast)
        meta = dico["meta"]
        blocks = dico["blocks"]
        # os.mkdir('./trash/')
        content = []
        reset = 0
        for block in track(blocks):
            # print(block)
            if block['t'] == 'Header':
                level = block['c'][0]
                if level <= 2:
                    if content != []:
                        # slice = pandoc.types.Pandoc(meta, content)
                        slice = {
                            'pandoc-api-version': self.pandoc_version,
                            'meta': self.meta,
                            'blocks': content,
                        }
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
                        pypandoc.convert_text(
                            json.dumps(slice),
                            outputfile = file,
                            format = "json",
                            to='html',
                            extra_args = [
                                "--standalone",
                                "--katex",
                                # "--filter=pandoc-plot",
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
                                "--filter=pandoc-sidenote" # the filter is not yet compatible with the latest version of pandoc
                            ])
                    key = block['c'][1][0]
                    mylevel = level
            content.append(block)

        with open('./structure_dict.json', 'w') as f:
            f.write(json.dumps(self.structure_dict))

    def generate_index(self):
        pypandoc.convert_text(
            self.ast,
            format='json',
            to='html',
            outputfile = self.dest_path + '/index.html',
            extra_args = [
                "--template="+self.dest_path+"_assets/templates/template-index.html"
            ]
        )

    def generate_404():
        pass

    def to_latex(self):
        if not os.path.exists(self.latex_path):
            os.mkdir(self.latex_path)
        pypandoc.convert_text(
            self.ast,
            format = 'json',
            to = 'latex',
            outputfile = self.latex_path + 'main.tex',
            extra_args = [
                "--metadata-file=_assets/meta/meta.yaml",
                "--standalone",
                "--filter=pandoc-crossref",
                "--bibliography=_assets/refs/refs.json",
                "--citeproc",
                "--number-sections",
            ]
        )


    def to_html(self):

        self.ast_html = self.ast

        self.pandoc_version = json.loads(self.ast_html)['pandoc-api-version']
        self.meta = json.loads(self.ast_html)['meta']

        self.abbreviation_dict = {}
        self.link_dict = {}
        self.path = ['', '']
        self.structure_list = []

        self.build_folder_structure()

        dico = json.loads(self.ast_html)
        meta_before = dico["meta"]

        # meta = self.ast_html[0] # saving metadata bc it seems overriden by --metadata-file

        self.pipe(
            [
                "--metadata-file=_assets/meta/meta.yaml",
                "--csl=_assets/refs/for-the-web.csl",
                # "--filter=_assets/filters/title_above_references.py",
                # "--number-sections",
                "--katex",
                # "--filter=pandoc-xnos",
                # "--filter=pandoc-secnos",
                "--filter=pandoc-crossref",
                "--bibliography=_assets/refs/refs.json",
                "--citeproc",
            ]
        )

        # print(doc.ast_html)

        # self.ast_html[0] = pandoc.types.Meta(doc.ast_html[0][0] | meta[0]) # merge yaml block with metadata from metadata file

        dico = json.loads(self.ast_html)

        self.meta = dico["meta"] | meta_before

        dico["meta"] = self.meta

        self.ast_html = json.dumps(dico)

        self.filter([
            self.add_title_to_references,
            self.get_abbreviation_dict,
            self.replace_abbreviations,
            self.generate_link_dict,
            self.links_filter
        ])

        self.generate_nav()
        self.filter([self.graphs_filter])
        self.split_structure()

        self.split()

        self.generate_index()

        # pandoc.write(
        #     self.ast_html,
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


def main():

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="Path to a Markdown source file.")

    args = parser.parse_args()

    args.markdown_source = os.path.abspath(args.markdown_source)

    # print(args.markdown_source)

    doc = Document(args.markdown_source)

    doc.to_latex()

    doc.to_html()




if __name__=='__main__':
    main()