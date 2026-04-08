import shutil
import os
import sys
import pypandoc
import argparse
import re
import csv
import json
import pkg_resources
import pickle
import mpld3
import unicodedata
import xml.etree.ElementTree as et
# import plotly

# import plotly.tools as tls
import pandocfilters as pf  

from bs4 import BeautifulSoup
from rich.progress import track
from urllib.parse import urlparse
from matplotlib.colors import to_hex
from matplotlib.pyplot import switch_backend

from .config import Config


ABOUT = "A single-source manuscript"
# SVG namespace for parsing
SVG_NS = {"svg": "http://www.w3.org/2000/svg"}

# Mapping from colors to CSS variables
COLOR_REPLACEMENTS = {
    "#000000": "var(--color-text)",
    "#00000000": "var(--color-text)",
    "#000": "var(--color-text)",
    "rgb(0,0,0)": "var(--color-text)",
    "rgb(0%,0%,0%)": "var(--color-text)"
}


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
        
        # switch_backend('agg')

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
            
    def write_abbreviations_file_latex(self):
        def simplify(text):
            # Normalize to NFD (decomposes accented characters)
            text = unicodedata.normalize('NFD', text)
            # Remove combining marks (accents)
            text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
            # Convert to lowercase
            text = text.lower()
            # Keep only lowercase letters and digits
            text = re.sub(r'[^a-z0-9]', '', text)
            return text
        
        with open(os.path.join(self.out_latex_path, 'abbr.tex'), 'w', encoding="utf-8") as f:
            f.write('\\makeglossaries\n')
            for key, val in self.abbreviation_dict.items():
                template = f'''\\newacronym{{{simplify(key)}}}{{{key}}}{{{val}}}\n'''
                f.write(template)

    def replace_abbreviations_html(self, key, value, format_, meta):
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
                 
    def replace_abbreviations_latex(self, key, value, format_, meta):
        def simplify(text):
            # Normalize to NFD (decomposes accented characters)
            text = unicodedata.normalize('NFD', text)
            # Remove combining marks (accents)
            text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
            # Convert to lowercase
            text = text.lower()
            # Keep only lowercase letters and digits
            text = re.sub(r'[^a-z0-9]', '', text)
            return text
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
                        abbr_latex = f'\\gls{{{simplify(abbr_text)}}}{following_char}'
                        return pf.RawInline('latex', abbr_latex)
                            
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
                    
                # Convert HTML to plain text
                content = pypandoc.convert_text(section, format='html', to='plain')

                # Remove lines that are likely image references (Markdown-style)
                content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
                
                # Remove table-like lines (pipes, pluses, colons, and dashes)
                content = '\n'.join(
                    line for line in content.split('\n')
                    if not re.match(r'^\s*[\|+: -]{3,}\s*$', line)
                )

                # Remove separators like *** or ---
                content = '\n'.join(
                    line for line in content.split('\n') 
                    if not re.match(r'^\s*([-*]){3,}\s*$', line)
                )

                # Collapse extra whitespace
                content = ' '.join(content.split())    
                
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


    def set_default_black(self, el):
        # Elements that are usually stroked (lines, outlines)
        tag = el.tag.split("}")[-1]  # strip namespace if present
        if tag == "text":
            style = el.get("style", "")
            if "fill" not in style and "fill" not in el.attrib:
                el.set("fill", "#000000")

    def replace_color(self, el):
        """Replace fill/stroke colors and inline styles if they match COLOR_REPLACEMENTS."""
        # Normalize and replace direct attributes
        for attr in ("fill", "stroke"):
            if attr in el.attrib:
                val = el.attrib[attr].strip().lower()
                if val in COLOR_REPLACEMENTS:
                    el.attrib[attr] = COLOR_REPLACEMENTS[val]

        # Replace colors in inline style
        if "style" in el.attrib:
            style = el.attrib["style"]

            def repl(m):
                prop, val = m.groups()
                val_norm = val.strip().lower()
                new_val = COLOR_REPLACEMENTS.get(val_norm, val)
                return f"{prop}:{new_val}"

            # Match fill:... or stroke:... ignoring spaces
            style = re.sub(r"(fill|stroke)\s*:\s*([^;]+)", repl, style)
            el.attrib["style"] = style

    def modify_svg_colors(self, svg_path):
        """Read SVG, replace colors, return modified SVG as string without ns0:svg junk."""
        try:
            # Parse
            tree = et.parse(svg_path)
            root = tree.getroot()

            # Strip all namespace prefixes
            for elem in root.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]  # remove namespace
                # Also clean attributes with namespaces
                for attr in list(elem.attrib):
                    if '}' in attr:
                        new_attr = attr.split('}', 1)[1]
                        elem.attrib[new_attr] = elem.attrib.pop(attr)

            # Replace colors
            for el in root.iter():
                # fill/stroke to black what's left blank
                self.set_default_black(el)
                self.replace_color(el)

            # Serialize back to string with plain <svg>
            return et.tostring(root, encoding="unicode", method="xml")
        except Exception as e:
            print(f"Error processing SVG {svg_path}: {e}")
            with open(svg_path, "r", encoding="utf-8") as f:
                return f.read()

            
    # SVG
    def inline_svg_filter(self, key, value, format, meta):
        if key == 'Image':
            # Safe unpacking
            attr = value[0]             # [id, classes, keyvals]
            caption = value[1] if len(value) > 1 else []
            target = value[2] if len(value) > 2 else ["", ""]  # [filename, type]
            filename, typef = target
            stuff = attr  # for compatibility with your previous code

            # Only process SVG files
            if filename.lower().endswith('.svg') and os.path.exists(filename):
                if filename.startswith('./'):
                    filename = filename[2:]

                # Extract classes from Pandoc attributes
                classes = stuff.get('classes', []) if isinstance(stuff, dict) else stuff[1]  # depends on pf version
                # Treat wwide as wide for HTML
                add_classes = [cls for cls in ('margin', 'wide') if cls in classes or (cls == 'wide' and 'wwide' in classes)]

                # Ensure output folder exists
                out_dir = os.path.join(self.out_html_path, '_assets', *os.path.split(filename)[:-1])
                os.makedirs(out_dir, exist_ok=True)

                # Copy original file to _assets
                out_svg_path = os.path.join(self.out_html_path, '_assets', filename)
                shutil.copyfile(filename, out_svg_path)

                # Modify the _assets copy in place
                modified_content = self.modify_svg_colors(out_svg_path)

                # Inject classes into <svg> tag
                if add_classes:
                    # If <svg> already has a class attribute, append
                    if 'class="' in modified_content:
                        def add_to_svg_class(match):
                            existing = match.group(1) or ''
                            existing_classes = existing.split()
                            for cls in add_classes:
                                if cls not in existing_classes:
                                    existing_classes.append(cls)
                            return f'class="{" ".join(existing_classes)}"'
                        modified_content = re.sub(r'class="([^"]*)"', add_to_svg_class, modified_content, count=1)
                    else:
                        # Insert new class attribute
                        modified_content = re.sub(r'<svg\b', f'<svg class="{" ".join(add_classes)}"', modified_content, count=1)

                print(f'Successfully processed SVG: {filename}')
                return pf.RawInline("html", modified_content)

        return None

    # GRAPHS
    
    # Plotly
    # def graphs_filter(self, key, value, format, meta):
    #     if key == 'Image':
    #         [ident, stuff, keyvals], caption, [filename, typef] = value
            
    #         if filename.endswith('.pkl'):
    #             with open(filename, 'rb') as f:
    #                 fig = pickle.load(f)
                
    #             all_labels = []
    #             all_colors = []
                
    #             lines_to_remove = []
    #             scatters_to_add = []

    #             # for ax in fig.get_axes():
    #             #     for line in ax.get_lines():
    #             #         marker = line.get_marker()
    
    #             #         # Skip 'None' markers (e.g. 'None', '', or ' ')
    #             #         if marker not in [None, 'None', '', ' ']:
    #             #             # Extract line data
    #             #             xdata = line.get_xdata()
    #             #             ydata = line.get_ydata()

    #             #             # Optional: Copy style from the line
    #             #             color = line.get_color()
    #             #             label = line.get_label()
    #             #             size = line.get_markersize()

    #             #             # Create scatter
    #             #             # scatter = ax.scatter(xdata, ydata, color=color, label=label, s=size**2)

    #             #             # Mark line for removal
    #             #             lines_to_remove.append(line)
                            
    #             #         all_labels.append(line.get_label())
    #             #         all_colors.append(to_hex(line.get_color()))
                        
    #             # for line in lines_to_remove:
    #             #     line.remove()
                        
    #             plotly_fig = tls.mpl_to_plotly(fig)
                
    #             plotly_fig.update_layout(
    #                 # showlegend=False,
    #                 template="none",  # Start from scratch (no theme)
    #                 xaxis=dict(
    #                     showline=True,
    #                     linecolor="black",
    #                     linewidth=.5,
    #                     gridcolor='rgba(0, 0, 0, 0.05)',
    #                     mirror=True,  # Show axis line on both bottom and top
    #                 ),
    #                 yaxis=dict(
    #                     showline=True,
    #                     linecolor="black",
    #                     linewidth=.5,
    #                     gridcolor='rgba(0, 0, 0, 0.05)',
    #                     mirror=True,  # Show axis line on both left and right
    #                 ),
    #                 paper_bgcolor='rgba(0,0,0,0)',
    #                 plot_bgcolor='rgba(0,0,0,0)'
    #             )
                
    #             plotly_fig.update_traces(line=dict(width=1.5))
    #             div = plotly.offline.plot(plotly_fig, include_plotlyjs=False, output_type='div', config= {'displayModeBar': False})
    #             return pf.RawInline("html", div)
    
    # MplD3
    def graphs_filter(self, key, value, format, meta):
        if key == 'Image':
            [ident, stuff, keyvals], caption, [filename, typef] = value
            
            if filename.endswith('.pkl'):
                with open(filename, 'rb') as f:
                    jsn = json.dumps(mpld3.fig_to_dict(pickle.load(f)))
                    
                graph_id = f"graph_{self.graph_count}"
                self.graph_count += 1
                graph_script = f"""
                var json_{graph_id} = {jsn};
                mpld3.draw_figure("{graph_id}", json_{graph_id});
                """

                return [
                    pf.RawInline("html", f"""
                        <div class='graph-container' id={graph_id}></div>
                        <script>{graph_script}</script>
                    """)
                ]       
                
        
    # # Dygraphs
    # def graphs_filter(self, key, value, format, meta):
    #     if key == 'Image':
    #         [ident, stuff, keyvals], caption, [filename, typef] = value
            
    #         if filename.split('.')[-1] == 'csv':
                
    #             # parsing the data
    #             with open(filename, newline='', encoding='utf-8') as f:
    #                 reader = csv.reader(f)
    #                 columns = next(reader)
    #             xcolumn = columns[0]
    #             ycolumns = ', '.join(columns[1:])
    #             kwargs = {}
    #             kwargs['x'] = xcolumn
    #             kwargs['y'] = ycolumns
    #             kwargs['kmb'] = 'true'
    #             kwargs['legendPosition'] = 'caption'
    #             kwargs['scales'] = 'linlin'
    #             for keyval in keyvals:
    #                 kwargs[keyval[0]] = keyval[1]
    #             if "xlabel" not in kwargs:
    #                 kwargs['xlabel'] = kwargs['x']
    #             if "ylabel" not in kwargs:
    #                 kwargs['ylabel'] = kwargs['y'].split(', ')[0]

    #             # formatting the graph  
    #             graph_id = f"dygraph_{self.graph_count}"
    #             self.graph_count += 1
                
    #             if(filename.startswith('./')):
    #                 filename = filename[2:]
                
    #             os.makedirs(os.path.join(self.out_html_path, '_assets', *os.path.split(filename)[:-1]), exist_ok=True)
    #             out_data_path = os.path.join(self.out_html_path, '_assets', f'{filename[:-4]}-graph_{self.graph_count}.csv')
    #             shutil.copyfile(filename, out_data_path)
                
    #             # # Copy CSV file to assets
    #             self.rearrange_columns(filename, out_data_path, [kwargs['x']] + kwargs['y'].split(', '))
                
    #             # Create graph script with proper relative paths
    #             graph_script = f""" 
    #                 var {graph_id} = generateGraph(id="{graph_id}", 
    #                     data="/_assets/{filename[:-4]}-graph_{self.graph_count}.csv", 
    #                     xlabel="{kwargs['xlabel']}", 
    #                     ylabel="{kwargs['ylabel']}", 
    #                     legendPosition="{kwargs['legendPosition']}",
    #                     kmb="{kwargs['kmb']}",
    #                     scales="{kwargs['scales']}"
    #                 );
    #             """
                
    #             graph_script = 'document.addEventListener("DOMContentLoaded", (event) => {' + graph_script + '});'
                
    #             # Save script file
    #             # graph_file = os.path.join(graphs_dir, f'graph{self.graph_count}.js')
    #             # with open(graph_file, 'w', encoding='utf-8') as f:
    #             #     f.write(graph_script)
                
    #             # Use relative path in script tag
    #             return [
    #                 pf.RawInline("html", f"""
    #                     <div class='graph-container' id={graph_id} legendPosition={kwargs['legendPosition']}></div>
    #                     <script>{graph_script}</script>
    #                 """)
    #             ]

    def assets_paths_filter(self, key, value, _fmt, _meta):
        if key == 'Image':
            [ident, stuff, keyvals], caption, [filename, typef] = value
            newfilename = 'assets/'+filename
            return pf.Image([ident, stuff, keyvals], caption, [newfilename, typef])
        
    def image_filter_latex(self, key, value, fmt, meta):
        if key != "Image":
            return

        [[ident, classes, kvs], alt, [src, title]] = value

        root, ext = os.path.splitext(src)

        # Copy image to output folder (if it exists locally)
        target_path = os.path.join(self.out_latex_path, src)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, target_path)
    
    def custom_figure(self, key, value, format, meta):
        if key == 'Figure':    
            # print()
            # print(key)
            # print(value)

            identifier = value[0][0]
            caption_block = value[1][1]  # the inlines of the caption
            img_block = value[2][0]['c'][0]  # the Image itself
            img_attr, img_caption, (src, title) = img_block['c']
            classes = img_attr[1]
            
            
            # print(img_caption)
            
            # print(classes)
            
            image = pf.Plain([pf.Image(img_attr, img_caption, (src, title))])
            
            def caption(type):
                return pf.Plain([pf.RawInline('latex', f'\\{type}{{')] + img_caption + [pf.RawInline('latex', f'\\label{{{identifier}}}}}')])

            # Decide LaTeX environment
            if 'wwide' in classes:
                # Use hvfloat for wwide class - full page width figure with optimal placement
                # hvFloat syntax: \hvFloat[options]{float-type}{object}[short-cap]{long-cap}{label}
                # We'll use doublePage option for full width, with caption on right
                
                return [
                    pf.RawBlock('latex', f'\\hvFloat[capWidth=w,capPos=right]{{figure}}{{\\includegraphics{{{src}}}}}[]{{'),
                    pf.Plain(img_caption),
                    pf.RawBlock('latex', f'}}{{{identifier}}}'),
                ]
            elif 'wide' in classes:
                env = 'figure*'
                opt = ''
                img = image, caption('caption')

            elif 'margin' in classes:
                env = 'wrapfigure'
                opt = '{O}{\\ssphdwrapfig}'
                img = image, caption('caption')
            else:
                env = 'figure'
                opt = ''
                img = image, caption('caption')
                return [
                    pf.RawBlock('latex', '\\begin{figure*}'),
                    pf.RawBlock('latex', '\\checkoddpage\\ifoddpage'),
                    pf.RawBlock('latex', '\\begin{minipage}[t]{\\ssphdfigwidth}\\vspace{0pt}\\par'),
                    image,
                    pf.RawBlock('latex', '\\end{minipage}\\hfill\\begin{minipage}[t]{\\ssphdcapwidth}\\vspace{\\ssphdmarginparsep}\\par'),
                    caption('caption'),
                    pf.RawBlock('latex','\\end{minipage}'),
                    pf.RawBlock('latex', '\\else'),
                    pf.RawBlock('latex', '\\begin{minipage}[t]{\\ssphdcapwidth}\\vspace{\\ssphdmarginparsep}\\par'),
                    caption('caption'),
                    pf.RawBlock('latex', '\\end{minipage}\\hfill\\begin{minipage}[t]{\\ssphdfigwidth}\\vspace{0pt}\\par'),
                    image,
                    pf.RawBlock('latex','\\end{minipage}'),
                    pf.RawBlock('latex', '\\fi'),
                    pf.RawBlock('latex', '\\end{figure*}')
                ]
                         
            return [
                pf.RawBlock('latex', f'\\begin{{{env}}}{opt}'),
                *img,
                pf.RawBlock('latex', f'\\end{{{env}}}'),
            ]
                    

    def subfigures_filter_latex(self, key, value, fmt, meta):
        if key == "Div":
            [[ident, classes, kvs], contents] = value
            if "subfigures" in classes:
                # print('---')
                # print(key)
                # print(value)
                # print()
                # print()
                
                # Extract caption from contents
                caption_block = None
                image_blocks = []
                
                for block in contents:
                    if block["t"] in ("Para", "Plain"):
                        inlines = block["c"]
                        images = [c for c in inlines if c["t"] == "Image"]
                        # If this block has images, it's an image row
                        if len(images) > 0:
                            image_blocks.append(block)
                        # Otherwise it might be a caption
                        elif caption_block is None and len(inlines) > 0:
                            caption_block = block
                
                # Process image blocks
                new_contents = []
                for block in image_blocks:
                    inlines = block["c"]
                    images = [c for c in inlines if c["t"] == "Image"]
                    n = len(images)
                    new_inlines = []
                    for j, img in enumerate(images):
                        attr, alt, target = img["c"]

                        kvs_dict = dict(attr[2])
                        if "width" not in kvs_dict:
                            # reduce a bit for gaps
                            kvs_dict["width"] = f"{(100 - (n-1)*2)/n:.0f}%"
                        attr[2] = list(kvs_dict.items())
                        img["c"] = [attr, alt, target]

                        new_inlines.append(img)
                        if j < n - 1:
                            # add small horizontal space between images
                            new_inlines.append(
                                pf.RawInline("latex", "\\hfill")
                            )

                    block["c"] = new_inlines
                    new_contents.append(block)
                    # add vertical space after this row
                    new_contents.append(
                        pf.RawBlock("latex", "\\medskip")
                    )
                
                # Build the figure* environment with caption at bottom
                result = [pf.RawBlock('latex', '\\begin{figure*}[t]')]
                result.extend(new_contents)
                
                # Add caption at the bottom if it exists
                if caption_block:
                    result.append(pf.RawBlock('latex', '\\caption{'))
                    result.append(caption_block)
                    result.append(pf.RawBlock('latex', f'\\label{{{ident}}}}}'))
                elif ident:
                    # If no caption but has an ID, still add label
                    result.append(pf.RawBlock('latex', f'\\label{{{ident}}}'))
                
                result.append(pf.RawBlock('latex', '\\end{figure*}'))
                
                return result

    def table_filter_latex(self, key, value, fmt, meta):
        if key == 'Div':
            try:
                if value[1][0]['t'] == 'Table':
                    [[ident, classes, kvs], contents] = value
                    if 'wide' in classes:
                        return ([
                            pf.RawBlock('latex', '\\begin{fullwidth}'),
                            pf.Div([ident, classes, kvs], contents),
                            pf.RawBlock('latex', '\\end{fullwidth}')
                        ])
                    elif 'margin' in classes:
                        return ([
                            pf.RawBlock('latex', '\\begin{marginpar}'),
                            pf.Div([ident, classes, kvs], contents),
                            pf.RawBlock('latex', '\\end{marginpar}')
                        ])
            except Exception: return None
            
    def replace_hrule(self, key, value, fmt, meta):
        if key == 'HorizontalRule':
            return pf.RawBlock('latex', '\\begin{center}\\vskip 15mm\\large\\noindent\\textbf{*~~*~~*}\\vskip 15mm\\end{center}')
            
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
                if section["section"]["level"] == "1":
                    process_section(section, None)
            # Process the root section and its subsections
            
            return transformed
        
        # Remove old root_path variable and use self.out_html_path instead
        # if os.path.exists(self.out_html_path):
        #     shutil.rmtree(self.out_html_path)
        os.makedirs(self.out_html_path, exist_ok=True)
        # os.makedirs(os.path.join(self.out_html_path, '_assets', 'graphs'), exist_ok=True)
        shutil.copytree(self.css_path, os.path.join(self.out_html_path, '_assets', 'css'), dirs_exist_ok=True)
        shutil.copytree(self.js_path, os.path.join(self.out_html_path, '_assets', 'js'), dirs_exist_ok=True)
        shutil.copytree(self.fonts_path, os.path.join(self.out_html_path, '_assets', 'fonts'), dirs_exist_ok=True)
        
        # generate files
        template_name = os.path.join(self.templates_path, 'template-section.html')
        
        # check if temp folder already exists
        shutil.rmtree('-/', ignore_errors=True)
        
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

        # Build a map of figure/table IDs to their containing sections
        self.id_to_section = {}
        for file in os.listdir('-/'):
            if file.endswith('.html'):
                section_id = file.split('/')[-1][:-5]
                if section_id == 'index':
                    section_id = '-index'
                with open(f'-/{file}', 'r', encoding='utf-8') as f:
                    temp_soup = BeautifulSoup(f, 'html.parser')
                    # Find all elements with IDs starting with fig: or tbl:
                    for elem in temp_soup.find_all(id=True):
                        elem_id = elem.get('id', '')
                        if elem_id.startswith('fig:') or elem_id.startswith('tbl:'):
                            self.id_to_section[elem_id] = section_id

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
                    soup = self.post_process_html(soup, titles, paths)
                
                if file == 'index.html':
                    with open(os.path.join(self.out_html_path, 'index.html'), 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                else:
                    output_path = os.path.join(self.out_html_path, self.structure[file[:-5]]["path"], 'index.html')
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))

        shutil.rmtree('-/')
        
        # if os.path.exists(os.path.join(self.root_path, 'tmp', 'data')):
        #     shutil.copytree(os.path.join(self.root_path, 'tmp', 'data'), os.path.join(self.out_html_path, '_assets', 'data'))
        #     shutil.rmtree('tmp')
        
    def post_process_html(self, soup, titles, paths):
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
            # print(link["href"]);print()
            href = link["href"]
            
            # Handle bare anchor links (like #fig:test or #tbl:test)
            if href.startswith('#'):
                anchor_id = href[1:]  # Remove the #
                if anchor_id in self.id_to_section:
                    target_section = self.id_to_section[anchor_id]
                    if target_section == '-index':
                        newhref = '/' + href
                    else:
                        newhref = self.structure[target_section]["path"] + '/' + href
                    link["href"] = newhref
                continue
            
            section_id = href.split('#')[0][:-5]
    
            if section_id in self.structure:
                if len(href.split('#')) > 1:
                    anchor = '#'+href.split('#')[1]
                    if section_id == anchor[1:]:
                        newhref = self.structure[section_id]["path"]
                    else:
                        newhref = self.structure[section_id]["path"] + '/' + anchor
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
        
            existing_secnum_span = heading.find("span", class_="header-section-number")

            # Extract section number from the existing span if present
            secnum = existing_secnum_span.text.strip() if existing_secnum_span else None

            # Create a new span for the title
            title_span = soup.new_tag("span", **{"class": "header-section-title"})

            # Move all children of the header into title_span, except the section number span
            for child in list(heading.contents):
                if child is not existing_secnum_span:  # Skip section number span
                    title_span.append(child.extract())

            # Clear existing contents and add structured spans
            heading.clear()
            if existing_secnum_span:
                heading.append(existing_secnum_span)
            heading.append(title_span)
        
            parent = heading.find_parent()
            
            if parent and parent.has_attr('id'):
                section_id = parent['id']
                
                anchor = soup.new_tag('a', href=soup.new_string(self.structure[section_id]["path"]))
                anchor.string = '#'
                anchor['class'] = 'heading-anchor'
                
                heading.insert(0, anchor)  # Insert anchor before the heading text  
        
        # wrap tables in wrappers
        for table in soup.find_all('table'):
            
            # tweak for subifigures
            subfigures = table.find_parent('figure')
            if subfigures:
                try:
                    del table.attrs["style"]
                except Exception: pass
                # get the element right after the table
                if "wide" in subfigures.get("class", []):
                    next_elem = table.find_next_sibling()
                    # if it's a figcaption, move it before the table
                    if next_elem and next_elem.name == "figcaption":
                        subfigures.insert(subfigures.contents.index(table), next_elem.extract())
                continue


            wrapper = soup.new_tag('div', **{'class': 'table-wrapper'})
            table.insert_before(wrapper)
            
            wrapper.append(table)
            
        # link images
        for image in soup.find_all('img'):
            if image.has_attr('src'):
                pth = image['src']
                # print("\nfigure\n")
                # print(pth)
                if pth.startswith('./'):
                    pth = pth[2:]
                image['src'] = os.path.join('_assets', pth)
                
        # undo svg dimensions
        for svg in soup.find_all('svg'):
            svg.attrs.pop('height', None)
            svg.attrs.pop('width', None)
        
        return soup
    
    def generate_404(self):
        pass


    def generate_bib_file(self, json_path):
        
        print(f"found CSL JSON: {json_path}")
        
        """
        Convert a CSL-JSON file to a BibTeX file using Pandoc.
        Returns the path to the generated .bib file.
        """
        # Build output path: mirror subfolders inside self.out_latex_path
        rel_path = os.path.relpath(json_path, self.root_path)
        bib_path = os.path.join(self.out_latex_path, os.path.splitext(rel_path)[0] + ".bib")

        # Make sure parent directories exist
        os.makedirs(os.path.dirname(bib_path), exist_ok=True)

        # Convert using Pandoc
        pypandoc.convert_file(json_path, 'biblatex', outputfile=bib_path, format='csljson')
        print(f"Generated bib file: {bib_path}")
        
        return bib_path.replace('\\', '/')


    def references_section_latex(self, key, value, format_, meta):
        if key == "Div" and "refs" in value[0][0]:
            return pf.RawBlock("latex", r"\loadgeometry{wide}\printbibheading[heading=bibintoc, title={References}]\begin{multicols}{2}\setstretch{1.2}\printbibliography[heading=none]\end{multicols}\loadgeometry{margins}")
        
    
    def abbr_section_latex(self, key, value, format_, meta):
        if key == "Div" and "abbr" in value[0][0]:
            return pf.RawBlock("latex", r"\loadgeometry{wide}\printglossary[title={Index of acronyms}, type=\acronymtype]\loadgeometry{margins}")

    def to_latex(self):
        if not os.path.exists(self.out_latex_path):
            os.mkdir(self.out_latex_path)   

        args = [
            f"--metadata-file={os.path.join(self.meta_path, 'meta.yaml')}",
            "--standalone",
            "--filter=pandoc-crossref",
            "--top-level-division=chapter",
            "--toc",
            "--number-sections",
            f"--template={os.path.join(self.templates_path, 'template-la.tex')}",
        ]

        if self.refs_file:
            print(self.refs_file)
            args.append("--biblatex")
            args.append(f"--metadata=bibfile:{self.generate_bib_file(self.refs_file)}")


        with open("./test.json", "w", encoding="utf-8") as f:
            f.write(self.ast)
            
        self.abbreviation_dict = {}

        
        # Apply the Python filter to the AST
        self.ast_latex = self.filter([
            self.get_abbreviation_dict,
            self.replace_abbreviations_latex,
            self.image_filter_latex,
            self.custom_figure,
            self.subfigures_filter_latex,
            self.table_filter_latex,
            self.references_section_latex,
            self.abbr_section_latex,
            self.replace_hrule
        ],self.ast)
        
        self.write_abbreviations_file_latex()

        # Convert the filtered AST, not the original
        pypandoc.convert_text(
            self.ast_latex,
            format="json",
            to="latex",
            outputfile=os.path.join(self.out_latex_path, f"{self.base_name}.tex"),
            extra_args=args,
        )
        
        # bookbinding
        with open(os.path.join(self.out_latex_path, f"{self.base_name}_signatures.tex"), 'w') as f:
            f.write(f'''
\\documentclass[b5paper]{{scrartcl}}
\\usepackage{{pdfpages}}
\\begin{{document}}
\\includepdf[pages=-, signature=16, landscape]{{{self.base_name}.pdf}}
\\end{{document}}
            ''')
        
    def to_html(self):

        self.ast_html = self.ast

        self.pandoc_version = json.loads(self.ast_html)['pandoc-api-version']
        self.meta = json.loads(self.ast_html)['meta']

        self.abbreviation_dict = {}

        dico = json.loads(self.ast_html)
        meta_before = dico["meta"]

        self.pipe([
            f"--metadata-file={os.path.join(self.meta_path, 'meta.yaml')}",
            "--filter=pandoc-crossref",
        ])
        
        if (self.refs_file):
            self.pipe([
                f"--bibliography={self.refs_file}",
                f"--csl={os.path.join(self.csl_path, 'for-the-web.csl')}",
                "--citeproc"
            ])
            # self.filter([self.hyperlink_title_filter]) # transforms all references titles to hyperlinks
        
        
        # Re-parse from updated AST after pandoc-crossref
        dico = json.loads(self.ast)
        # append doc meta to metadata file
        self.meta = dico["meta"] | meta_before
        dico["meta"] = self.meta
        self.ast_html = json.dumps(dico)
    
        self.filter([
            self.add_title_to_references,
            self.get_abbreviation_dict,
            self.replace_abbreviations_html,
            self.graphs_filter,
            self.inline_svg_filter,
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