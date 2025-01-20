import shutil
import os  # kept for other potential os operations
import pypandoc
import argparse
import re
import json
from jsonschema import validate, ValidationError
from yaml import safe_load
import pathlib as pl

import pandocfilters as pf

from rich.progress import track

# from inspect import getsourcefile
# from pandoc.types import Pandoc, Header, MetaType, MetaInlines, MetaBool, Str
# from mpld3 import plugins


ABOUT = "The ultimate document processor."

class ParseConfig:
    def __init__(self, config: str, schema_file: str) -> None:
        current_root = pl.Path(config).parent

        # Load config and schema
        with open(config, 'r') as file:
            self.config = safe_load(file)

        with open(schema_file, 'r') as schema_file:
            self.schema = json.load(schema_file)

        self.properties = self.schema.get('properties', {})

        # Enforce schema validation
        try:
            validate(instance=self.config, schema=self.schema)
        except ValidationError as e:
            raise ValueError(f"Config file does not match schema: {e.message}") from e
        except Exception as e:
            raise ValueError(f"An error occurred while validating the config file: {e}") from e

        # Check root directory
        self.root = self.config.get('root')
        if not self.root:
            raise KeyError("The configuration file must include the 'root' key.")
        if not pl.Path(current_root / self.root).exists():
            raise FileNotFoundError(f"Root directory '{self.root}' does not exist.")

        self.root = pl.Path(current_root / self.root)

        self.output = self.config.get('output')
        if not self.output:
            raise KeyError("The configuration file must include the 'output' key.")
        if not pl.Path(current_root / self.output).exists():
            raise FileNotFoundError(f"Output directory '{self.output}' does not exist.")
        
        # Construct paths
        for key, value in self.config.items():
            if key == 'root' or key == 'output':
                continue

            # Construct path from root and value (relative path)
            path = pl.Path(self.root) / value

            # If the path doesn't exist, print a warning
            if not path.exists():
                print(f"Warning: Path '{path}' does not exist.")
            
            # Set the key as an attribute of the class
            setattr(self, key, path)

    def __str__(self):
        # Everyhing except self.properties, self.schema and self.config
        string = [f"{key}: {value}" for key, value in self.__dict__.items() if key not in ('properties', 'schema', 'config')]
        return '\n'.join(string)
    
class Document:

    def __init__(self, source: str, config: str) -> None:
        self.source_file = source

        try:
            # Get absolute path of the script
            script_path = pl.Path(__file__).resolve()
            script_dir = script_path.parent
            parser = ParseConfig(config, script_dir / 'config_schema.json')
        except Exception as e:
            print(e)
            exit(1)

        source_root = pl.Path(config).parent

        self.root           = parser.root
        self.dest_path      = parser.output
        self.meta_file      = parser.meta
        self.templates_path = parser.templates
        self.css_path       = parser.css
        self.pictures_path  = parser.graphics
        self.refs_path      = parser.references
        self.latex_path     = parser.latex

        try:
            with open(source, 'r') as file:
                self.source = file.read()
        except Exception as e:
            print(e)
            exit(1)
        

        self.ast = pypandoc.convert_file(
                self.source_file,
                'json',
                extra_args = [
            ])

        self.graph_count = 0

    ## FILTERS

    def add_title_to_references(self, key: str, value: list, format_: str, meta: dict) -> list:
        if key == "Div" and "refs" in value[0][0]:
            attrs, children = value
            t1 = ["unnumbered"]
            t2 = []
            title = pf.Header(1, ["references", t1, t2], [pf.Str("References")])
            return [title, pf.Div(attrs, children)]

    def get_abbreviation_dict(self, key: str, value: list, format_: str, meta: dict) -> list:
        abbr_def_pattern = r'\+\[(.*?)\]:\s(.*?)$'
        if key == 'Para':
            text = pf.stringify(value)
            match = re.match(abbr_def_pattern, text)
            if match:
                abbreviation, description = match.groups()
                self.abbreviation_dict[abbreviation] = description
                return []

    def replace_abbreviations(self, key: str, value: str, format_: str, meta: dict) -> list:
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

    def generate_link_dict(self, key: str, value: list, format_: str, meta: dict) -> None:

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

    def links_filter(self, key: str, value: list, format_: str, meta: dict) -> list:
        if key == 'Link':
            [t1, linktext, [href, t4]] = value
            ref = href[1:]
            if ref in self.link_dict:
                newhref = self.link_dict[ref]
                return pf.Link(t1, linktext, [newhref, t4])

    def nav_filter(self, key: str, value: list, format_: str, meta: dict) -> list:
        if key == 'BulletList':
            items = []
            for element in value:
                id = element[0]['c'][0]['c'][0][4:]
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

    def copy(self, ast: str, opts: list) -> str:
        return pypandoc.convert_text(
            ast,
            to='json',
            format='json',
            extra_args=opts)

    def pipe(self, opts: list) -> None:
        self.ast = self.copy(
            self.ast,
            opts)

    def filter(self, handles: list, ast: str = None) -> str:
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

    def build_folder_structure(self) -> None:
        if not self.dest_path.exists():
            shutil.copytree(self.root, self.dest_path)

    # SEARCH

    def generate_search_index(self, key: str, value: list, format_: str, meta: dict) -> None:

        self.search_dict = {}

        if key == 'Header':
             [level, [label, t1, t2], header] = value

        elif key == 'Paragraph':
            pass

    # STRUCTURE

    def generate_nav(self) -> None:
        print("generating nav")
        self.nav = pypandoc.convert_text(
            self.ast,
            format = "json",
            to="html",
            extra_args=[
                "--number-sections",
                f"--template={self.templates_path / 'template-toc.html'}",
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
            outputfile = self.templates_path / "nav.html",
            # extra_args=[
            #     "--number-sections",
            #     "--template="+self.templates_path+"/template-toc.html",
            # ]
        )

    def extract_structure(self) -> None:
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

    def split_structure(self) -> None:
        print("generating split structure")
        for key, val in track(self.structure_dict.items()):
            id = key
            level = val["level"]
            if level == 1:
                chapter_path = self.dest_path / key
                if not chapter_path.exists():
                    chapter_path.mkdir()
                for child in val["children"]:
                    child_path = chapter_path / child
                    if not child_path.exists():
                        child_path.mkdir()

    # GRAPHS
    def graphs_filter(self, key: str, value: list, format: str, meta: dict) -> list:
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
                graphsjs_file = self.dest_path / "graphs.js"
                with open(graphsjs_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(graph_script)
                return [
                    pf.RawInline("html", f"<div class='graph-container' id={graph_id} legendPosition={kwargs['legendPosition']}></div>")
                ]

    def get_next(self, key: str) -> tuple:
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

    def get_prev(self, key: str) -> tuple:
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

    def split(self) -> None:
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
                            file = f"{self.dest_path}{key}/index.html"
                            ischapter = "true"
                            parent = ""
                            parenttitle = ""
                        elif mylevel == 2:
                            file = f"{self.dest_path}{self.structure_dict[key]['parent']}/{key}/index.html"
                            ischapter = ""
                            parent = self.structure_dict[key]["parent"]
                            parenttitle = f"{self.structure_dict[parent]['number']} {self.structure_dict[parent]['title']}"
                        pypandoc.convert_text(
                            json.dumps(slice),
                            outputfile = file,
                            format = "json",
                            to='html',
                            extra_args = [
                                "--standalone",
                                "--katex",
                                f"--template={self.dest_path / 'templates/template-section.html'}",
                                "--variable=base=/",
                                f"--variable=pagetitle={pagetitle}",
                                f"--variable=ischapter:{ischapter}",
                                f"--variable=parent={parent}",
                                f"--variable=parenttitle={parenttitle}",
                                f"--variable=hasprev={hasprev}",
                                f"--variable=prev={prev}",
                                f"--variable=prevtitle={prevtitle}",
                                f"--variable=hasnext={hasnext}",
                                f"--variable=next={next}",
                                f"--variable=nexttitle={nexttitle}",
                                "--number-sections",
                                f"--number-offset={offset.replace('.', ',')}",
                                "--toc-depth=3",
                                "--section-divs",
                                "--filter=pandoc-sidenote" # the filter is not yet compatible with the latest version of pandoc
                            ])
                    key = block['c'][1][0]
                    mylevel = level
            content.append(block)

        with open('./structure_dict.json', 'w') as f:
            f.write(json.dumps(self.structure_dict))

    def generate_index(self) -> None:
        pypandoc.convert_text(
            self.ast,
            format='json',
            to='html',
            outputfile = self.dest_path / 'index.html',
            extra_args = [
                "--template="+str(self.dest_path / "templates/template-index.html")
            ]
        )

    def generate_404(self) -> None:
        pass

    def to_latex(self) -> None:
        if not self.latex_path.exists():
            self.latex_path.mkdir()

        print (self.meta_file)
        pypandoc.convert_text(
            self.ast,
            format = 'json',
            to = 'latex',
            outputfile = self.latex_path / 'main.tex',
            extra_args = [
                f"--metadata-file={self.meta_file}/meta.yaml",
                "--standalone",
                "--filter=pandoc-crossref",
                f"--bibliography={self.refs_path / 'refs.json'}",
                "--citeproc",
                "--number-sections",
            ]
        )


    def to_html(self) -> None:

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
        print (self.meta_file)
        self.pipe(
            [
                f"--metadata-file={self.meta_file}",
                f"--csl={self.refs_path / 'for-the-web.csl'}",
                "--katex",
                # "--filter=pandoc-xnos",
                # "--filter=pandoc-secnos",
                "--filter=pandoc-crossref",
                f"--bibliography={self.refs_path / 'refs.json'}",
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

def build(source: str, config: str) -> None:
    doc = Document(source, config)
    doc.to_latex()
    doc.to_html()

def main() -> None:

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="Path to a Markdown source file.")
    parser.add_argument("config", help="Path to the configuration file.")

    args = parser.parse_args()
    build(args.markdown_source, args.config)

if __name__ == '__main__':
    main()