import shutil
import os
import sys
import pypandoc
import argparse
import re
import csv
import json
import pkg_resources

import pandocfilters as pf

from lunr import lunr
from bs4 import BeautifulSoup
from rich.progress import track
from urllib.parse import urlparse

from .config import Config


ABOUT = "A single-source manuscript"


class Document:

    def __init__(self, source, config_file=None, split_level=2, toc_level=3, refs_file=None):
        self.config = Config(config_file)
        # Use config's validation method
        self.config.validate_file(source)
        
        self.package_path   = pkg_resources.resource_filename('ssphd', '')
        self.filters_path   = os.path.join(self.package_path, 'filters')

        self.source_file    = os.path.abspath(source)
        self.root_path      = os.path.dirname(os.path.abspath(self.source_file))
        
        # Get base name without extension
        self.base_name = os.path.splitext(os.path.basename(self.source_file))[0]
        
        # Create output paths using config and base name
        self.out_html_path      = os.path.join(self.root_path, 'out/'+self.base_name, self.config.get_path('output_html'))
        self.out_latex_path     = os.path.join(self.root_path, 'out/'+self.base_name, self.config.get_path('output_latex'))
        
        # Use config paths
        self.templates_path     = os.path.join(self.package_path, self.config.get_path('templates'))
        self.css_path           = os.path.join(self.package_path, self.config.get_path('css'))
        self.fonts_path         = os.path.join(self.package_path, self.config.get_path('fonts'))
        self.js_path            = os.path.join(self.package_path, self.config.get_path('js'))
        self.refs_file          = refs_file
        self.csl_path           = os.path.join(self.package_path, self.config.get_path('csl'))
        self.meta_path          = os.path.join(self.package_path, self.config.get_path('meta'))
        
        # split/toc levels
        self.split_level        = int(split_level)
        self.toc_level          = int(toc_level)

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
        
        search_template = os.path.join(self.templates_path, 'template-search-section.html')
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
                
        with open(f"{os.path.join(self.out_html_path, '_assets', 'documents.json')}", 'w', encoding='utf-8') as f:
            json.dump(self.search_documents, f, indent=4)
                
        shutil.rmtree('-/')
        
    
    def rearrange_columns(self, input_csv, output_csv, columns_order):
        # Open the input CSV file for reading
        with open(input_csv, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)

            # Open the output CSV file for writing
            with open(output_csv, mode='w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=columns_order)
                writer.writeheader()  # Write the header with the new column order

                # Write the rows with the columns rearranged
                for row in reader:
                    reordered_row = {col: row[col] for col in columns_order}
                    writer.writerow(reordered_row)

    # GRAPHS
    def graphs_filter(self, key, value, format, meta):
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
                kwargs['x'] = xcolumn
                kwargs['y'] = ycolumns
                kwargs['legendPosition'] = 'graph'
                kwargs['kmb'] = 'true'
                for keyval in keyvals:
                    kwargs[keyval[0]] = keyval[1]
                if "xlabel" not in kwargs:
                    kwargs['xlabel'] = kwargs['x']
                if "ylabel" not in kwargs:
                    kwargs['ylabel'] = kwargs['y'].split(', ')[0]

                # formatting the graph
                graph_id = f"dygraph_{self.graph_count}"
                self.graph_count += 1
                
                # Ensure the graphs directory exists
                data_dir = os.path.join(self.root_path, 'tmp', 'data')
                os.makedirs(data_dir, exist_ok=True)
                
                # # Copy CSV file to assets
                self.rearrange_columns(filename, os.path.join(data_dir, f'{os.path.basename(filename)[:-4]}-graph_{self.graph_count}.csv'), [kwargs['x']] + kwargs['y'].split(', '))
                
                # Create graph script with proper relative paths
                graph_script = f""" 
                    var {graph_id} = generateGraph(id="{graph_id}", 
                        data="/_assets/data/{os.path.basename(filename)[:-4]}-graph_{self.graph_count}.csv", 
                        xlabel="{kwargs['xlabel']}", 
                        ylabel="{kwargs['ylabel']}", 
                        legendPosition="{kwargs['legendPosition']}",
                        kmblabels={kwargs["kmb"]}
                    );
                """
                
                graph_script = 'document.addEventListener("DOMContentLoaded", (event) => {' + graph_script + '});'
                
                # Save script file
                # graph_file = os.path.join(graphs_dir, f'graph{self.graph_count}.js')
                # with open(graph_file, 'w', encoding='utf-8') as f:
                #     f.write(graph_script)
                
                # Use relative path in script tag
                return [
                    pf.RawInline("html", f"""
                        <div class='graph-container' id={graph_id} legendPosition={kwargs['legendPosition']}></div>
                        <script>{graph_script}</script>
                    """)
                ]

    def assets_paths_filter(self, key, value, _fmt, _meta):
        if key == 'Image':
            [ident, stuff, keyvals], caption, [filename, typef] = value
            newfilename = 'assets/'+filename
            return pf.Image([ident, stuff, keyvals], caption, [newfilename, typef])

    def chunk(self):
        
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
                    dr = os.path.join(self.out_html_path, section_id)
                    parent_id = "-index"
                    if not os.path.exists(dr):
                        os.makedirs(dr)
                elif level <= self.split_level:
                    path = transformed[parent_id].get("path") + '/' + section_id
                    dr = os.path.join(self.out_html_path, transformed[parent_id].get("path"), section_id)
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

            for section in track(input_json["subsections"], description = 'Extracting structure'):
                process_section(section, None)
            # Process the root section and its subsections
            
            return transformed
        
        # Remove old root_path variable and use self.out_html_path instead
        if os.path.exists(self.out_html_path):
            shutil.rmtree(self.out_html_path)
        os.makedirs(self.out_html_path)
        # os.makedirs(os.path.join(self.out_html_path, '_assets', 'graphs'), exist_ok=True)
        shutil.copytree(self.css_path, os.path.join(self.out_html_path, '_assets', 'css'))
        shutil.copytree(self.js_path, os.path.join(self.out_html_path, '_assets', 'js'))
        shutil.copytree(self.fonts_path, os.path.join(self.out_html_path, '_assets', 'fonts'))
        
        # generate files
        template_name = os.path.join(self.templates_path, 'template-section.html')
        pypandoc.convert_text(
            self.ast,
            format='json',
            to='chunkedhtml',
            extra_args=[
                '--toc',
                f'--toc-depth={self.toc_level}',
                f'--split-level={self.split_level}',
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

        self.structure = transform_sitemap(sitemap)
        
        self.structure["-index"] = {
            "title": 'index',
            "level": 0,
            "path": '',
            "number": None,
            "parent": None,
            "children": [key for key in self.structure if self.structure[key]["level"] == 1]
        }

        for file in track(os.listdir('-/'), description='Building output tree'):
            
            if os.path.isdir(file):  # Only process directories
                shutil.copytree(file, os.path.join(self.out_html_path, '_assets', file), dirs_exist_ok=True)  # Copy subfolder
            
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
                    
                    soup = self.post_process(soup, titles, paths)
                
                if file == 'index.html':
                    with open(os.path.join(self.out_html_path, 'index.html'), 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                else:
                    output_path = os.path.join(self.out_html_path, self.structure[file[:-5]]["path"], 'index.html')
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))

        shutil.rmtree('-/')
        
        if os.path.exists(os.path.join(self.root_path, 'tmp', 'data')):
            shutil.copytree(os.path.join(self.root_path, 'tmp', 'data'), os.path.join(self.out_html_path, '_assets', 'data'))
            shutil.rmtree('tmp')
        
    def post_process(self, soup, titles, paths):
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
                    
            # append external to external link
            def is_external_link(ref):
                parsed_link = urlparse(ref)
                return bool(parsed_link.netloc)  # If netloc is present, it's an external link

            if is_external_link(href):
                if 'class' in link.attrs:
                    link['class'].append('external')
                else:
                    link['class'] = ['external']
                            
        # header anchors
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            parent = heading.find_parent()
            
            if parent and parent.has_attr('id'):
                section_id = parent['id']
                
                anchor = soup.new_tag('a', href=soup.new_string(self.structure[section_id]["path"]))
                anchor.string = '#'
                anchor['class'] = 'heading-anchor'
                
                heading.insert(0, anchor)  # Insert anchor before the heading text  
        
        # wrap tables in wrappers
        for table in soup.find_all('table'):
            if table.find_parent('figure'):
                continue  # Skip tables inside <figure>

            wrapper = soup.new_tag('div', **{'class': 'table-wrapper'})
            table.insert_before(wrapper)
            
            wrapper.append(table)
            
        # link images
        for image in soup.find_all('img'):
            if image.has_attr('src'):
                pth = image['src']
                if pth.startswith('./'):
                    pth = pth[2:]
                image['src'] = os.path.join('_assets', pth)
                
        return soup
    
    def generate_404(self):
        pass

    def to_latex(self):
        if not os.path.exists(self.out_latex_path):
            os.mkdir(self.out_latex_path)
        args = [
                f"--metadata-file={os.path.join(self.meta_path, 'meta.yaml')}",
                "--standalone",
                "--filter=pandoc-crossref",
                "--top-level-division=chapter",
                "--number-sections",
                f"--template={os.path.join(self.templates_path, 'template-la.tex')}"
            ]
        if (self.refs_file):
            args.append(f"--bibliography={self.refs_file}")
            args.append("--citeproc")
        pypandoc.convert_text(
            self.ast,
            format = 'json',
            to = 'latex',
            outputfile = os.path.join(self.out_latex_path, f'{self.base_name}.tex'),
            extra_args = args
        )

    def to_html(self):

        self.ast_html = self.ast

        self.pandoc_version = json.loads(self.ast_html)['pandoc-api-version']
        self.meta = json.loads(self.ast_html)['meta']

        self.abbreviation_dict = {}

        dico = json.loads(self.ast_html)
        meta_before = dico["meta"]

        self.pipe([
            f"--metadata-file={os.path.join(self.meta_path, 'meta.yaml')}",
            f"--csl={self.csl_path}/for-the-web.csl",
            "--filter=pandoc-crossref",
        ])
        
        if (self.refs_file):
            self.pipe([
                f"--bibliography={self.refs_file}",
                "--citeproc",
            ])
        
        # append doc meta to metadata file
        self.meta = dico["meta"] | meta_before
        dico["meta"] = self.meta
        self.ast_html = json.dumps(dico)
    
        self.filter([
            self.add_title_to_references,
            self.get_abbreviation_dict,
            self.replace_abbreviations,
            self.graphs_filter,
        ])
        
        self.chunk()
        self.generate_search_index()


def main():
    
    def file_path(path):
        if os.path.isfile(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument("markdown_source", help="path to a Markdown source file")
    parser.add_argument("--config", "-c", help="path to config YAML file", type=file_path)
    parser.add_argument("--split-level", "-s", help="depth of split for HTML output", default=2, type=int)
    parser.add_argument("--toc-level", "-t", help="depth of TOC", default=3, type=int)
    parser.add_argument("--refs", "-r", help="references JSON file", type=file_path)
    parser.add_argument("--html", "-H", help="enables HTML output", action="store_true", default=False)
    parser.add_argument("--latex", "-L", help="enables LaTeX output", action="store_true", default=False)
    args = parser.parse_args()

    if not(args.html or args.latex):
        print("Please give an output format. Example: --html.")
        sys.exit(2)
    else:
        try:
            doc = Document(args.markdown_source, args.config, args.split_level, args.toc_level, args.refs)
            if(args.html):
                print("Converting to HTML...")
                doc.to_html()
            if(args.latex):
                print("Converting to LaTeX...")
                doc.to_latex()
            sys.exit(0)
        except (FileNotFoundError, ValueError, PermissionError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


if __name__=='__main__':
    main()