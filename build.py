import shutil
import os
import pypandoc
import argparse
import re
import json

import pandocfilters as pf
from bs4 import BeautifulSoup
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

    # SEARCH
    def generate_search_index(self, key, value, format_, meta):

        self.search_dict = {}

        if key == 'Header':
             [level, [label, t1, t2], header] = value

        elif key == 'Paragraph':
            pass

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
                
    def chunk_link_filter(self, key, value, _fmt, meta):
        if key == 'Link':
            [t1, linktext, [href, t4]] = value
            print()
            print(f'oldlink: {href}')
            section_id = href.split('#')[0][:-5]
            print(f'section id: {section_id}')
            if section_id in self.structure:
                anchor = href.split('#')[1]
                print(f'anchor: {anchor}')
                newhref = self.structure[anchor]["path"]
                print(f'newlink: {newhref}')
                return pf.Link(t1, linktext, [newhref, t4])
                
    def chunk(self, splitLevel=4, tocLevel=6):
        
        def transform_sitemap(input_json):
            if not os.path.exists(root_path):
                os.mkdir('chunking-test')
            def process_section(section, parent_id):
                section_id = section["section"]["id"]
                if not section_id:
                    return {}
                # create paths and folder structure
                level = int(section["section"]["level"])
                
                if level == 1:
                    path = section_id
                    dr = root_path + '/' + section_id
                    parent_id = "-index"
                    if not os.path.exists(dr):
                        os.mkdir(dr)
                elif level <= splitLevel:
                    path = transformed[parent_id].get("path") + '/' + section_id
                    dr = root_path +'/'+ transformed[parent_id].get("path") + '/' + section_id
                    if not os.path.exists(dr):
                        os.mkdir(dr)
                else:
                    path = transformed[parent_id].get("path").split('/#')[0] + '/#' + section_id

                print(path)

                # Add the current section
                transformed[section_id] = {
                    "title": section["section"]["title"],
                    "level": level,
                    "path": path,
                    "number": section["section"].get("number"),
                    "parent": parent_id,
                    "children": []
                }
                
                for subsection in section.get("subsections", []):
                    child_id = subsection["section"]["id"]
                    if child_id:
                        transformed[section_id]["children"].append(child_id)
                        process_section(subsection, section_id)

            transformed = {}

            for section in track(input_json["subsections"]):
                process_section(section, None)
            # Process the root section and its subsections
            
            return transformed
        
        root_path = 'test-html'
        if os.path.exists(f'{root_path}'):
            shutil.rmtree(f'{root_path}')
        os.mkdir(f'{root_path}')
        shutil.copytree('_assets/', f'{root_path}/_assets')
        
        # pre filters
        self.filter(
            [self.add_title_to_references]
        )
        
        # generate files
        pypandoc.convert_text(
            self.ast,
            format='json',
            to='chunkedhtml',
            extra_args=[
                '--toc',
                f'--toc-depth={tocLevel}',
                f'--split-level={splitLevel}',
                '--chunk-template=%i.html',
                '--number-sections',
                '--section-divs',
                '--filter=pandoc-sidenote',
                f'--template=template-section.html',
                '--variable=base=/'
            ]
        )

        with open('-/sitemap.json', 'r', encoding='utf-8') as f:
            sitemap = json.load(f)
        
        # shutil.rmtree('-/')
        
        self.structure = transform_sitemap(sitemap)
        
        self.structure["-index"] = {
            "title": 'index',
            "level": 0,
            "path": '',
            "number": None,
            "parent": None,
            "children": [key for key in self.structure if self.structure[key]["level"] == 1]
        }
        
        with open('./structure_dict.json', 'w', encoding="utf-8") as f:
            json.dump(self.structure, f, indent=4, ensure_ascii="false")
    
        
        # putting the files in the
        for file in track(os.listdir('-/')):
            if file.endswith('.html') and file != 'index.html':
                section_id = file.split('/')[-1][:-5]
                ids = []
                titles = []
                paths = []
                while section_id != '-index':
                    ids.insert(0, section_id)
                    if self.structure[section_id]["number"]:
                        name = self.structure[section_id]["number"] + ' ' + self.structure[section_id]["title"]
                    else:
                        name = self.structure[section_id]["title"]
                    titles.insert(0, name)
                    section_id = self.structure[section_id]["parent"]
                for iid in ids:
                    paths.append(self.structure[iid]["path"])
                with open(f'-/{file}', 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    breadcrumbs = soup.find('div', class_='breadcrumbs')
                    if breadcrumbs:
                        home = soup.new_tag('a', href='')
                        homebtn = soup.new_tag('i', **{'class': 'bx bx-home-alt-2'})
                        home.append(homebtn)
                        breadcrumbs.append(home)
                        for title, path in zip(titles, paths):
                            separator = soup.new_tag('span',  **{'class': 'separator'})
                            separator.string = '/'
                            item = soup.new_tag('a', href=path)
                            item.string = title                         
                            breadcrumbs.append(separator)
                            breadcrumbs.append(item)
                with open(f'-/{file}', 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                        
                with open(f'-/{file}', 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    for link in soup.find_all("a", href=True):
                        href = link["href"]
                        section_id = href.split('#')[0][:-5]
                        if section_id in self.structure:
                            if len(href.split('#')) > 1:
                                anchor = '#'+href.split('#')[1]
                            else:
                                anchor = ''
                            newhref = self.structure[section_id]["path"] + anchor
                            link["href"] = newhref
                
                if file == 'index.html':
                    with open(f'-/{file}', f'{root_path}/{file}', 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                else:
                    with open(f'{root_path}/{self.structure[file[:-5]]["path"]}/index.html', 'w', encoding='utf-8') as f:
                        f.write(str(soup))

        shutil.rmtree('-/')
        
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

        dico = json.loads(self.ast_html)
        meta_before = dico["meta"]

        self.pipe(
            [
                "--metadata-file=_assets/meta/meta.yaml",
                "--csl=_assets/refs/for-the-web.csl",
                "--filter=pandoc-crossref",
                "--bibliography=_assets/refs/refs.json",
                "--citeproc",
            ]
        )
        

        # append doc meta to metadata file
        dico = json.loads(self.ast_html)
        self.meta = dico["meta"] | meta_before
        dico["meta"] = self.meta
        self.ast_html = json.dumps(dico)
    
        self.filter([
            self.get_abbreviation_dict,
            self.replace_abbreviations
        ])
        self.chunk()


def main():

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="Path to a Markdown source file.")

    args = parser.parse_args()

    args.markdown_source = os.path.abspath(args.markdown_source)

    # print(args.markdown_source)

    doc = Document(args.markdown_source)

    # doc.to_latex()

    doc.to_html()




if __name__=='__main__':
    main()