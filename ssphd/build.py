import shutil
import os
import pypandoc
import argparse
import re
import json
import pkg_resources

import pandocfilters as pf

from lunr import lunr
from bs4 import BeautifulSoup
from rich.progress import track

from .config import Config

import sys

ABOUT = "The ultimate document processor."


class Document:

    def __init__(self, source, config_file=None):
        self.config = Config(config_file)
        # Use config's validation method
        self.config.validate_file(source)
        
        self.package_path = pkg_resources.resource_filename('ssphd', '')
        self.filters_path = os.path.join(self.package_path, 'filters')

        self.source_file    = os.path.abspath(source)
        self.root_path      = os.path.dirname(os.path.abspath(self.source_file))
        
        # Get base name without extension
        base_name = os.path.splitext(os.path.basename(self.source_file))[0]
        
        # Create output paths using config and base name
        self.dest_path      = os.path.join(self.root_path, 'output/'+base_name, self.config.get_path('output_html'))
        self.latex_path     = os.path.join(self.root_path, 'output/'+base_name, self.config.get_path('output_latex'))
        
        # Use config paths
        self.assets_path    = os.path.join(self.root_path, self.config.get_path('assets'))
        self.templates_path = os.path.join(self.root_path, self.config.get_path('templates'))
        self.css_path       = os.path.join(self.root_path, self.config.get_path('css'))
        self.pictures_path  = os.path.join(self.root_path, self.config.get_path('pictures'))
        self.refs_path      = os.path.join(self.root_path, self.config.get_path('refs'))
        self.meta_path      = os.path.join(self.root_path, self.config.get_path('meta'))

        self.ast = pypandoc.convert_file(
                self.source_file,
                format='markdown+smart+emoji',
                to='json',
                extra_args = []
            )

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
                if (abbr_end > abbr_start + 2):
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

    def remove_header_filter(self, key, value, format, meta):
        if key == 'Header':
            return pf.Null

    # SEARCH
    def generate_search_index(self):

        self.search_documents = []
        
        search_template = self.config.get_template_path('template-search-section.html')
        pypandoc.convert_text(
            self.ast,
            format='json',
            to='chunkedhtml',
            extra_args=[
                '--chunk-template=%i.html',
                '--split-level=6',
                f'--template={search_template}',
                '--katex',
            ]
        )
        
        for file in track(os.listdir('-/'), description='Generating search index'):
            if file.endswith('.html') and file != 'index.html':
                with open(f'-/{file}', 'r', encoding='utf-8') as f:
                    section = f.read() 
                content = ' '.join(pypandoc.convert_text(
                    section,
                    format='html',
                    to='plain',
                ).split('\n')[2:-1])
                section_id = file.split('/')[-1][:-5]
                title = self.structure[section_id]["title"]
                number = self.structure[section_id]["number"]
                path = self.structure[section_id]["path"]
                level = self.structure[section_id]["level"]
                
                document = {
                    "link": path,
                    "title": title,
                    "level": level,
                    "number": number,
                    "content": content,
                }
                
                self.search_documents.append(document)
                
        with open(f'{self.dest_path}/_assets/documents.json', 'w', encoding='utf-8') as f:
            json.dump(self.search_documents, f, indent=4)
        
        # pre-building index
        # index = lunr(
        #     ref="link",
        #     fields=[{
        #             "field_name": "title", "boost": 10,
        #         },{
        #             "field_name": "content", "boost": 1,
        #     }],
        #     documents=self.search_documents
        # )        
        # with open(f'{self.dest_path}/_assets/index.json', 'w', encoding='utf-8') as f:
        #     json.dump(index.serialize(), f, ensure_ascii=False)
                
        shutil.rmtree('-/')

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
                
                # formatting the graph
                graph_id = f"dygraph_{self.graph_count}"
                self.graph_count += 1
                
                # Ensure the graphs directory exists
                graphs_dir = os.path.join(self.dest_path, '_assets', 'graphs')
                os.makedirs(graphs_dir, exist_ok=True)
                
                # Copy CSV file to assets
                csv_dest = os.path.join(self.dest_path, '_assets', 'data', os.path.basename(filename))
                os.makedirs(os.path.dirname(csv_dest), exist_ok=True)
                shutil.copy2(filename, csv_dest)
                
                # Create graph script with proper relative paths
                graph_script = f"""
                    var {graph_id} = generateGraph(id="{graph_id}", 
                        data="../data/{os.path.basename(filename)}", 
                        xdata="{xcolumn}", 
                        ydata="{ycolumns}", 
                        xlabel="{kwargs['xlabel']}", 
                        ylabel="{kwargs['ylabel']}", 
                        legendPosition="{kwargs['legendPosition']}"
                    );
                """
                
                # Save script file
                graph_file = os.path.join(graphs_dir, f'graph{self.graph_count}.js')
                with open(graph_file, 'w', encoding='utf-8') as f:
                    f.write(graph_script)
                
                # Use relative path in script tag
                return [
                    pf.RawInline("html", f"""
                        <div class='graph-container' id={graph_id} legendPosition={kwargs['legendPosition']}></div>
                        <script src="../_assets/graphs/graph{self.graph_count}.js"></script>
                    """)
                ]

    def chunk(self, splitLevel=2, tocLevel=3):
        
        def transform_sitemap(input_json):
            # Remove the chunking-test check - it was a development artifact
            transformed = {}
            
            def process_section(section, parent_id):
                section_id = section["section"]["id"]
                if not section_id:
                    return {}
                # create paths and folder structure
                level = int(section["section"]["level"])
                
                if level == 1:
                    path = section_id
                    dr = os.path.join(self.dest_path, section_id)
                    parent_id = "-index"
                    if not os.path.exists(dr):
                        os.makedirs(dr)
                elif level <= splitLevel:
                    path = transformed[parent_id].get("path") + '/' + section_id
                    dr = os.path.join(self.dest_path, transformed[parent_id].get("path"), section_id)
                    if not os.path.exists(dr):
                        os.makedirs(dr)
                else:
                    path = transformed[parent_id].get("path").split('/#')[0] + '/#' + section_id

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

            for section in track(input_json["subsections"]):
                process_section(section, None)
            # Process the root section and its subsections
            
            return transformed
        
        # Remove old root_path variable and use self.dest_path instead
        if os.path.exists(self.dest_path):
            shutil.rmtree(self.dest_path)
        os.makedirs(self.dest_path)
        os.makedirs(os.path.join(self.dest_path, '_assets', 'graphs'), exist_ok=True)
        os.makedirs(os.path.join(self.dest_path, '_assets', 'data'), exist_ok=True)
        shutil.copytree('_assets/', os.path.join(self.dest_path, '_assets'), dirs_exist_ok=True)
        
        # generate files
        template_name = self.config.get_template_path('template-section.html')
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
                "--filter=pandoc-sidenote",
                f'--template={template_name}',
                '--variable=base=/',
                '--katex',
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
        
        # with open('./structure_dict.json', 'w', encoding="utf-8") as f:
        #     json.dump(self.structure, f, indent=4, ensure_ascii="false")

        for file in track(os.listdir('-/')):
            
            #converting index.html
            if file.endswith('.html'):
                section_id = file.split('/')[-1][:-5]
                if section_id=='index':
                    section_id = '-index'
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
                    
                    # breadcrumbs
                    breadcrumbs = soup.find('div', class_='breadcrumbs')
                    if breadcrumbs:
                        for title, path in zip(titles, paths):
                            separator = soup.new_tag('span',  **{'class': 'separator'})
                            separator.string = '/'
                            item = soup.new_tag('a', href=path)
                            item.string = title                         
                            breadcrumbs.append(separator)
                            breadcrumbs.append(item)
                            
                    # link replacement
                    for link in soup.find_all("a", href=True):
                        href = link["href"]
                        section_id = href.split('#')[0][:-5]
                        if section_id in self.structure:
                            if len(href.split('#')) > 1:
                                anchor = '#'+href.split('#')[1]
                                if section_id == anchor[1:]:
                                    newhref = self.structure[section_id]["path"]
                                else:
                                    newhref = self.structure[section_id]["path"] + anchor
                            else:
                                newhref = self.structure[section_id]["path"]
                            link["href"] = newhref
                
                if file == 'index.html':
                    with open(os.path.join(self.dest_path, 'index.html'), 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                else:
                    output_path = os.path.join(self.dest_path, self.structure[file[:-5]]["path"], 'index.html')
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
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
            self.add_title_to_references,
            self.get_abbreviation_dict,
            self.replace_abbreviations,
        ])
        
        self.chunk()
        
        self.generate_search_index()


def main():

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="Path to a Markdown source file.")
    parser.add_argument("--config", "-c", help="Path to config YAML file")

    args = parser.parse_args()

    try:
        doc = Document(args.markdown_source, args.config)
        doc.to_html()
    except (FileNotFoundError, ValueError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__=='__main__':
    main()