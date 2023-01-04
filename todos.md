# filter order

1. savelinkdict
2. xnos
3. links-filter
4. secnos
5. citeproc
6. global YAML (
   1. refs.json
   2. style.csl
   3. ...
   )
7. generate bibliography & list ofs
   (detect all cited references ?)


//SPLIT//

1. `--number-section`
2. local YAML (w/ number offset)
3. css
4. local json



# structure

- `index.html`

    Texte propre à l'index

- section folder (auto label name)
  - subsection folder (auto label name)

    each file has its own metadata block :

    ```yaml
    ---
    level: <0 (only for index.html) or 1 or 2>
    number-offset: 5,3 <- first is chapter offset, second is sec
    localtitle: <full title>
    label: <Pandoc-generated label name>
    up: <if level 2 -> link current chapter, if level 1 -> link to index>
    prev: <url of prev section>
    next: <url of next section>
    ---
    ```

- `_styles`
  - CSS stylesheets

- `_assets`
  - all assets

- `_meta`
  - `meta.yaml`
    ```yaml
    url: <url of index when deployed to the web>
    title:
    subtitle:
    auhor:
    date:
    lab:
    uni:
    supervisor:
        - karim
        - philippe
    jury: {
        - yop
        - yippidy
    }
    navigation: |
        <ul>
            ... nav ...
        </ul>
    ```
  - `nav.html`
  - `refs.json`
  - `style.csl`
  - `style_latex.csl`

- `_tex`
  - `tufte-style-thesis.cls`
  - `.tex` file & aux garbage

- `_dl`
  - `thesis.pdf`
  - `thesis.epub` ?
  - `thesis.docx` ?


# preprocessing

- secnos filter : -> `section_number = 1.8.5` in keyval pairs   (`Attr[1][2]`)
  (not if unnumbered (`Attr[1][1] == "unnumbered"`))

  **NOPE !** pandoc `--number-offset` option can take care of that :
  <https://pandoc.org/MANUAL.html#option--number-offset>

- generate nav & yaml

- imports in pfm ?


* * *


# todo

- rework crosslink filter w/ more proprer `Attr()` data type
- centralize all meta in yaml (global & local)
- create fixed index template (separated from section variables) w/ introductory text
- bibliography, list of figures & tables, glossary, index separated sections ?
- implement search through the whole page w/ JS ?